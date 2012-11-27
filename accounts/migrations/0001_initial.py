# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('accounts_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_date', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('real_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('earned', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=5, decimal_places=2)),
            ('rated', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('liked', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('commented', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('subscribed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('karma', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('accounts', ['User'])

        # Adding model 'InviteRequest'
        db.create_table('accounts_inviterequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_date', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('real_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=2048)),
        ))
        db.send_create_signal('accounts', ['InviteRequest'])

        # Adding model 'UserWhitelist'
        db.create_table('accounts_userwhitelist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_date', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('accounts', ['UserWhitelist'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table('accounts_user')

        # Deleting model 'InviteRequest'
        db.delete_table('accounts_inviterequest')

        # Deleting model 'UserWhitelist'
        db.delete_table('accounts_userwhitelist')


    models = {
        'accounts.inviterequest': {
            'Meta': {'object_name': 'InviteRequest'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'commented': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'earned': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'karma': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'liked': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'rated': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subscribed': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'accounts.userwhitelist': {
            'Meta': {'object_name': 'UserWhitelist'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['accounts']