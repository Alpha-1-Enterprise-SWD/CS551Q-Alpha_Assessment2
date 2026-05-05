import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import GPPractices, GPPractitioners, GPDetails, 
from catalog.utils import HB_LOOKUP, get_coordinates

class Command(BaseCommand):
    help = 'Import GP data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-path',
            type=str,
            default='data',
            help='Path to the data directory containing CSV files'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before importing'
        )

    def handle(self, *args, **options):
        data_path = options['data_path']
        clear_data = options['clear']
        
        self.stdout.write(self.style.SUCCESS('Starting GP data import...'))
        
        if clear_data:
            self.clear_existing_data()
        
        try:
            # Import practices
            self.import_practices(data_path)

            # Import practitioners
            self.import_gp_practitioners(data_path)
            
            # # Import GP details
            self.import_gp_details(data_path)
            
            # # Import population data
            self.import_populations(data_path)
            
            self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during import: {str(e)}'))
            raise

    def clear_existing_data(self):
        self.stdout.write('Clearing existing data...')
        GPPopulations.objects.all().delete()
        GPDetails.objects.all().delete()
        GPPractitioners.objects.all().delete()
        GPPractices.objects.all().delete()
        self.stdout.write('Existing data cleared.')

    def import_practices(self, data_path):
        self.stdout.write('Importing GP practices...')
        file_path = os.path.join(data_path, 'GPPractices.csv')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"GPPractices.csv not found in {data_path}")
        
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            with transaction.atomic():
                for row in reader:
                    

                    # Combine address fields
                    address_parts = []
                    if row.get('AddressLine2'):
                        address_parts.append(row['AddressLine2'])
                    if row.get('AddressLine3'):
                        address_parts.append(row['AddressLine3'])
                    address = ', '.join(address_parts)
                    
                    GPPractices.objects.update_or_create(
                        practice_code=row.get('PracticeCode', ''),
                        defaults={
                            'name': row.get('PracticeName', ''),
                            'list_size': int(row.get('PracticeListSize', 0)) if row.get('PracticeListSize') else 0,
                            'address': address,
                            'postcode': row.get('Postcode', ''),
                            'telephone': row.get('TelephoneNumber', ''),
                            'health_board': HB_LOOKUP.get(row.get('HB', ''), row.get('HB', '')),
                        }
                    )
                
                    # for p in GPPractices.objects.all():
                    #     print(f'{p.practice_code} | {p.name[:30]} | {p.postcode} | {p.list_size} | {p.address}')
        
        practice_count = GPPractices.objects.count()
        self.stdout.write(f'Imported {practice_count} GP practices.')

    def import_gp_practitioners(self, data_path):
        self.stdout.write('Importing GP Practitioners ...')
        file_path = os.path.join(data_path, 'GPPractitioners.csv')

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"GPPractitioners.csv not found in {data_path}")
        
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            with transaction.atomic():
                for row in reader:
                    try:
                        GPPractitioners.objects.update_or_create(
                            medical_council_number=row.get('GeneralMedicalCouncilNumber', ''),
                            defaults={
                                'forename': row.get('Forename', ''),
                                'middle_initial': row.get('MiddleInitial', '') or None,
                                'surname': row.get('Surname', ''),
                                'sex': row.get('Sex', '') or None
                            }
                        )
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f"Error importing GP {row.get('GeneralMedicalCouncilNumber', '')}: {e}")
                        )
                        continue
        
        practitioners_count = GPPractitioners.objects.count()
        self.stdout.write(f'Imported {practitioners_count} GP practitioners')

    def import_gp_details(self, data_path):
        self.stdout.write('Importing GP details...')
        file_path = os.path.join(data_path, 'GPDetails.csv')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"GPDetails.csv not found in {data_path}")
        
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            
            with transaction.atomic():
                for row in reader:
                    try:
                        gp = GPPractitioners.objects.get(medical_council_number=row.get('GeneralMedicalCouncilNumber', ''))
                        practice = GPPractices.objects.get(practice_code=row.get('PracticeCode', ''))

                        GPDetails.objects.update_or_create(
                            gp_code = gp,
                            practice=practice,
                            defaults= {
                                'designation': row.get('GPDesignation', ''),
                            }
                        )
                    except GPPractitioners.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Practitioner {row.get('GeneralMedicalCouncilNumber', '')} not found"
                            )
                        )
                        continue

                    except GPPractices.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Practice {row.get('PracticeCode', '')} not found"
                            )
                        )
                        continue
            # GPDetails_count = GPDetails.objects.all()
            # for p in GPDetails_count:
            #     print(p.medical_council_number)
        gp_count = GPDetails.objects.count()
        self.stdout.write(f'Imported {gp_count} GP details.')

    def import_populations(self, data_path):
        self.stdout.write('Importing population data...')
        file_path = os.path.join(data_path, 'GPPopulations.csv')
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"GPPopulations.csv not found in {data_path}")
        
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            
            with transaction.atomic():
                for row in reader:
                    try:
                        practice = GPPractices.objects.get(practice_code=row.get('PracticeCode', ''))
                        
                        # Create population record for each sex
                        GPPopulations.objects.update_or_create(
                            practice=practice,
                            sex=row.get('Sex', ''),
                            defaults={
                                'ages00to04': int(row.get('Ages00to04', 0)) if row.get('Ages00to04') else 0,
                                'ages05to09': int(row.get('Ages05to09', 0)) if row.get('Ages05to09') else 0,
                                'ages10to14': int(row.get('Ages10to14', 0)) if row.get('Ages10to14') else 0,
                                'ages15to19': int(row.get('Ages15to19', 0)) if row.get('Ages15to19') else 0,
                                'ages20to24': int(row.get('Ages20to24', 0)) if row.get('Ages20to24') else 0,
                                'ages25to29': int(row.get('Ages25to29', 0)) if row.get('Ages25to29') else 0,
                                'ages30to34': int(row.get('Ages30to34', 0)) if row.get('Ages30to34') else 0,
                                'ages35to39': int(row.get('Ages35to39', 0)) if row.get('Ages35to39') else 0,
                                'ages40to44': int(row.get('Ages40to44', 0)) if row.get('Ages40to44') else 0,
                                'ages45to49': int(row.get('Ages45to49', 0)) if row.get('Ages45to49') else 0,
                                'ages50to54': int(row.get('Ages50to54', 0)) if row.get('Ages50to54') else 0,
                                'ages55to59': int(row.get('Ages55to59', 0)) if row.get('Ages55to59') else 0,
                                'ages60to64': int(row.get('Ages60to64', 0)) if row.get('Ages60to64') else 0,
                                'ages65to69': int(row.get('Ages65to69', 0)) if row.get('Ages65to69') else 0,
                                'ages70to74': int(row.get('Ages70to74', 0)) if row.get('Ages70to74') else 0,
                                'ages75to79': int(row.get('Ages75to79', 0)) if row.get('Ages75to79') else 0,
                                'ages80to84': int(row.get('Ages80to84', 0)) if row.get('Ages80to84') else 0,
                                'ages85plus': int(row.get('Ages85plus', 0)) if row.get('Ages85plus') else 0,
                            }
                        )
                    except GPPractices.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Practice {row.get('PracticeCode', '')} not found for population data"
                            )
                        )
                        continue
        # GPPopulations_count = GPPopulations.objects.all()
        # for p in GPPopulations_count:
        #     print(p.practice.practice_code, p.sex)
        population_count = GPPopulations.objects.count()
        self.stdout.write(f'Imported {population_count} population records.')

    # def generate_summary(self):
    #     """Generate a summary of imported data"""
    #     practice_count = GPPractices.objects.count()
    #     gp_count = GPDetails.objects.count()
    #     population_count = GPPopulations.objects.count()
    #     total_patients = GPPractices.objects.aggregate(
    #         total=models.Sum('list_size')
    #     )['total'] or 0
        
    #     self.stdout.write('\n' + '='*50)
    #     self.stdout.write('IMPORT SUMMARY')
    #     self.stdout.write('='*50)
    #     self.stdout.write(f'Total Practices: {practice_count:,}')
    #     self.stdout.write(f'Total GPs: {gp_count:,}')
    #     self.stdout.write(f'Total Population Records: {population_count:,}')
    #     self.stdout.write(f'Total Patients: {total_patients:,}')
        
    #     if gp_count > 0:
    #         avg_ratio = total_patients / gp_count
    #         self.stdout.write(f'Average Patient/GP Ratio: {avg_ratio:.1f}')
        
    #     self.stdout.write('='*50)
