# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class Dialog
###########################################################################

class Dialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Application", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.MINIMIZE_BOX )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Input File" ), wx.VERTICAL )

		self.m_input_file = wx.FilePickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		sbSizer1.Add( self.m_input_file, 0, wx.ALL|wx.EXPAND, 5 )


		fgSizer1.Add( sbSizer1, 1, wx.EXPAND, 5 )

		sbSizer11 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Output Directory" ), wx.VERTICAL )

		self.m_output_dir = wx.DirPickerCtrl( sbSizer11.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		sbSizer11.Add( self.m_output_dir, 0, wx.ALL|wx.EXPAND, 5 )


		fgSizer1.Add( sbSizer11, 1, wx.EXPAND, 5 )

		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Actions" ), wx.VERTICAL )

		gSizer2 = wx.GridSizer( 0, 4, 0, 0 )

		self.m_start_button = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_start_button, 0, wx.ALL, 5 )

		self.m_save_button = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Save Config", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_save_button, 0, wx.ALL, 5 )

		self.m_exit_button = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_exit_button, 0, wx.ALL, 5 )

		self.m_help_button = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Help", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_help_button, 0, wx.ALL, 5 )


		sbSizer3.Add( gSizer2, 1, wx.EXPAND, 5 )


		fgSizer1.Add( sbSizer3, 1, wx.EXPAND, 5 )

		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Results" ), wx.VERTICAL )

		gSizer3 = wx.GridSizer( 0, 1, 0, 0 )

		self.m_status_message = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Waiting...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_status_message.Wrap( -1 )

		gSizer3.Add( self.m_status_message, 0, wx.ALL|wx.EXPAND, 5 )


		sbSizer4.Add( gSizer3, 1, wx.EXPAND, 5 )


		fgSizer1.Add( sbSizer4, 1, wx.EXPAND, 5 )


		self.SetSizer( fgSizer1 )
		self.Layout()
		fgSizer1.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.m_start_button.Bind( wx.EVT_BUTTON, self.OnStart )
		self.m_save_button.Bind( wx.EVT_BUTTON, self.OnSave )
		self.m_exit_button.Bind( wx.EVT_BUTTON, self.OnExit )
		self.m_help_button.Bind( wx.EVT_BUTTON, self.OnHelp )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()

	def OnStart( self, event ):
		event.Skip()

	def OnSave( self, event ):
		event.Skip()

	def OnExit( self, event ):
		event.Skip()

	def OnHelp( self, event ):
		event.Skip()


