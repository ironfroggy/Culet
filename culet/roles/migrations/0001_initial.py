# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Role'
        db.create_table('roles_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('role_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
        ))
        db.send_create_signal('roles', ['Role'])

        # Adding model 'RoleAction'
        db.create_table('roles_roleaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['roles.Role'])),
            ('action_module', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('action_class', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('roles', ['RoleAction'])

        # Adding model 'ModelPermission'
        db.create_table('roles_modelpermission', (
            ('role_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['roles.Role'], unique=True, primary_key=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('roles', ['ModelPermission'])

        # Adding model 'ItemPermission'
        db.create_table('roles_itempermission', (
            ('role_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['roles.Role'], unique=True, primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('roles', ['ItemPermission'])


    def backwards(self, orm):
        
        # Deleting model 'Role'
        db.delete_table('roles_role')

        # Deleting model 'RoleAction'
        db.delete_table('roles_roleaction')

        # Deleting model 'ModelPermission'
        db.delete_table('roles_modelpermission')

        # Deleting model 'ItemPermission'
        db.delete_table('roles_itempermission')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'roles.itempermission': {
            'Meta': {'object_name': 'ItemPermission', '_ormbases': ['roles.Role']},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'role_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['roles.Role']", 'unique': 'True', 'primary_key': 'True'})
        },
        'roles.modelpermission': {
            'Meta': {'object_name': 'ModelPermission', '_ormbases': ['roles.Role']},
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'role_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['roles.Role']", 'unique': 'True', 'primary_key': 'True'})
        },
        'roles.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'role_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']"})
        },
        'roles.roleaction': {
            'Meta': {'object_name': 'RoleAction'},
            'action_class': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'action_module': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': "orm['roles.Role']"})
        }
    }

    complete_apps = ['roles']
