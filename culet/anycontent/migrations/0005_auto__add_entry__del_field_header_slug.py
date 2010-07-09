# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Entry'
        db.create_table('anycontent_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anycontent.Header'])),
            ('stream', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['anycontent.Stream'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('anycontent', ['Entry'])

        # Deleting field 'Header.slug'
        db.delete_column('anycontent_header', 'slug')

        # Removing M2M table for field entries on 'Stream'
        db.delete_table('anycontent_stream_entries')


    def backwards(self, orm):
        
        # Deleting model 'Entry'
        db.delete_table('anycontent_entry')

        # Adding field 'Header.slug'
        db.add_column('anycontent_header', 'slug', self.gf('django.db.models.fields.SlugField')(default='x', max_length=100, unique=True, db_index=True), keep_default=False)

        # Adding M2M table for field entries on 'Stream'
        db.create_table('anycontent_stream_entries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('stream', models.ForeignKey(orm['anycontent.stream'], null=False)),
            ('header', models.ForeignKey(orm['anycontent.header'], null=False))
        ))
        db.create_unique('anycontent_stream_entries', ['stream_id', 'header_id'])


    models = {
        'anycontent.entry': {
            'Meta': {'unique_together': "(('stream', 'slug'),)", 'object_name': 'Entry'},
            'header': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anycontent.Header']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'stream': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['anycontent.Stream']"})
        },
        'anycontent.header': {
            'Meta': {'object_name': 'Header'},
            'content_id': ('django.db.models.fields.IntegerField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'content_type_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'anycontent.plaintext': {
            'Meta': {'object_name': 'PlainText'},
            'body': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'anycontent.stream': {
            'Meta': {'object_name': 'Stream'},
            'entries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['anycontent.Header']", 'through': "orm['anycontent.Entry']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['anycontent']
