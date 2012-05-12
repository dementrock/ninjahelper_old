# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MainScheduleCourse'
        db.create_table('schedule_mainschedulecourse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('friendly_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('course_id', self.gf('django.db.models.fields.IntegerField')()),
            ('course_ccn', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('schedule', ['MainScheduleCourse'])

        # Adding model 'ScheduleManager'
        db.create_table('schedule_schedulemanager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['community.UserProfile'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.MainScheduleCourse'])),
        ))
        db.send_create_signal('schedule', ['ScheduleManager'])


    def backwards(self, orm):
        
        # Deleting model 'MainScheduleCourse'
        db.delete_table('schedule_mainschedulecourse')

        # Deleting model 'ScheduleManager'
        db.delete_table('schedule_schedulemanager')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'community.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'cell_mail': ('django.db.models.fields.CharField', [], {'default': "'txt.att.net'", 'max_length': '100', 'blank': 'True'}),
            'cellphone': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '30', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_profile'", 'symmetrical': 'False', 'through': "orm['schedule.ScheduleManager']", 'to': "orm['schedule.MainScheduleCourse']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_short_code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'email_to_verify': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_verification_code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'friend': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'friend_rel_+'", 'to': "orm['community.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_email_set': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_friend_list_imported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_friend_schedule_imported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_main_schedule_imported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_phone_set': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ninjacourses_password': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'url_as_friend': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'schedule.mainschedulecourse': {
            'Meta': {'object_name': 'MainScheduleCourse'},
            'course_ccn': ('django.db.models.fields.IntegerField', [], {}),
            'course_id': ('django.db.models.fields.IntegerField', [], {}),
            'friendly_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'schedule.schedulemanager': {
            'Meta': {'object_name': 'ScheduleManager'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.MainScheduleCourse']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['community.UserProfile']"})
        }
    }

    complete_apps = ['schedule']
