# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Vote.source_ip'
        db.add_column('videos_vote', 'source_ip',
                      self.gf('django.db.models.fields.IPAddressField')(default='169.233.10.206', max_length=15),
                      keep_default=False)

        # Adding field 'Rating.source_ip'
        db.add_column('videos_rating', 'source_ip',
                      self.gf('django.db.models.fields.IPAddressField')(default='169.233.10.206', max_length=15),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Vote.source_ip'
        db.delete_column('videos_vote', 'source_ip')

        # Deleting field 'Rating.source_ip'
        db.delete_column('videos_rating', 'source_ip')


    models = {
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
        'videos.question': {
            'Meta': {'object_name': 'Question'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'time': ('django.db.models.fields.IntegerField', [], {}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videos.Video']"})
        },
        'videos.rating': {
            'Meta': {'object_name': 'Rating'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videos.Video']"})
        },
        'videos.video': {
            'Meta': {'object_name': 'Video'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'reward': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'yt_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'})
        },
        'videos.vote': {
            'Meta': {'object_name': 'Vote'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.User']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['videos.Video']"})
        }
    }

    complete_apps = ['videos']