# _*_ coding: utf-8 _*_

__author__ = 'PEICX'
__date__ = '2018/3/31 15:47'

from web_lib.parser.HtmlParser import HtmlParser


class documentParser:
	'''
	This class is a document parser
	'''
	def __init__(self,Response):
		try:
			parser = HtmlParser(Response)
		except:
			msg = 'There is no parser for "%s".' % Response.get_url()
			raise msg

		self._parser = parser

	def get_get_urls(self):
		return self._parser.get_get_urls()

	def get_form_reqs(self):
		return self._parser.get_form_reqs()

	def get_forms(self):
		return self._parser.get_forms()