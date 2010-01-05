from django.core.management.base import NoArgsCommand
from django.core.management.commands import inspectdb


class Command(NoArgsCommand):
    help="Displays list of models and it's objects count"
    
    def handle_noargs(self, **options):
        for line in self.handle_models():
            print line
        
    def handle_models(self):
        from django.db import connection
        table2model = lambda table_name: table_name.title().replace('_','').replace(' ','').replace('-','')
        connection_cursor = connection.cursor()
        for table_name in connection.introspection.get_table_list(connection_cursor):
            yield "class %s(models.Model)" % table2model(table_name)
            connection_cursor.execute("SELECT count(*) from %s" % table_name)
            row_count = connection_cursor.fetchall()
            row_count = row_count.pop()
            row_count = int(row_count[0])
            yield "Number of objects: %s" % row_count
             