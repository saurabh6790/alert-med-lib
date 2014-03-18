# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from install_erpnext import exec_in_shell
from webnotes.model.doc import addchild
from webnotes.model.bean import getlist
import os

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def show_sites(self):
		self.doclist=self.doc.clear_table(self.doclist,'site_status_details')
		for filename in os.listdir(self.doc.sites_path):
			sites = addchild(self.doc, 'site_status_details',
				'Site Status Details', self.doclist)
			sites.site_name = filename
			if filename[-1] != '1':
				sites.status = '1'

	def make_enable_dissable(self):
		for site in getlist(self.doclist, 'site_status_details'):
			#make dissable
			if site.status not in [1, '1'] and site.site_name[-1] != '1':
				exec_in_shell("mv %(path)s/%(site_name)s/ %(path)s/%(site_name)s1"%{'path':self.doc.sites_path,'site_name':site.site_name})

			#make enable
			if site.status == 1 and site.site_name[-1] == '1':
				new_site_name = site.site_name[:-1]
				exec_in_shell("mv %(path)s/%(site_name)s/ %(path)s/%(new_site_name)s"%{'path':self.doc.sites_path,'site_name':site.site_name, 'new_site_name':new_site_name})
		self.show_sites()
		self.doc.save()