# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.pp_email'
        db.add_column('accounts_user', 'pp_email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=254),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.pp_email'
        db.delete_column('accounts_user', 'pp_email')


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
        'accounts.payout': {
            'Meta': {'object_name': 'Payout'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"})
        },
        'accounts.user': {
            'Meta': {'object_name': 'User'},
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '5', 'decimal_places': '2'}),
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
            'pp_email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'rated': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subscribed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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