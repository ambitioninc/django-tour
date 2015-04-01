# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tour.complete_url'
        db.add_column(u'tour_tour', 'complete_url',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TourStatus.create_time'
        db.add_column(u'tour_tourstatus', 'create_time',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 4, 10, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'TourStatus.complete_time'
        db.add_column(u'tour_tourstatus', 'complete_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tour.complete_url'
        db.delete_column(u'tour_tour', 'complete_url')

        # Deleting field 'TourStatus.create_time'
        db.delete_column(u'tour_tourstatus', 'create_time')

        # Deleting field 'TourStatus.complete_time'
        db.delete_column(u'tour_tourstatus', 'complete_time')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tour.step': {
            'Meta': {'object_name': 'Step'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'parent_step': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_steps'", 'null': 'True', 'to': u"orm['tour.Step']"}),
            'step_class': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'tour': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tour.Tour']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'tour.tour': {
            'Meta': {'object_name': 'Tour'},
            'complete_url': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'tour_class': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': u"orm['tour.TourStatus']", 'symmetrical': 'False'})
        },
        u'tour.tourstatus': {
            'Meta': {'object_name': 'TourStatus'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'complete_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tour': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tour.Tour']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['tour']