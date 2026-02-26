from django.core.management.commands.migrate import Command as MigrateCommand

class Command(MigrateCommand):
    help = 'Migrate the database schema to the replica databases.'

    def handle(self, *args, **options):
      
        options['database'] = 'default'
        super().handle(*args, **options)

        
        for replica in ['replica_1', 'replica_2']:
            options['database'] = replica
            super().handle(*args, **options)
