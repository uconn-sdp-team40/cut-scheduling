import wx
import ProjectGUI
import configparser
import pathlib
import time
import hashlib
import threading
import math
from os import path

#############################
import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook

#Object for each order in Excel file
class CutOrder:

    def __init__(self, id, due_date, priority, vars_dict):
        self._id = id
        self._due_date = due_date
        self._priority = 1 if priority == 'High' else 0
        self._order_vars_dict = vars_dict
        self._oct = 0
        self._ost = 0
        self._tdt = 0
    
    def do_calcs(self, const_dict):
        # calculate OST, OCT, and TDT and update them
        # OST:
        MMT = const_dict['const_PST'] * self._order_vars_dict['spr_NM'] * 2
        MNT = const_dict['const_MST'] * self._order_vars_dict['spr_NM']
        MUT = const_dict['const_PST'] * self._order_vars_dict['spr_NM']
        MS = self._order_vars_dict['spr_TCY'] / const_dict['const_SS']
        MT = self._order_vars_dict['spr_TCY'] / (const_dict['const_ST'] * const_dict['const_STF'])
        MRT = (self._order_vars_dict['spr_TCL'] * 0.5) * (self._order_vars_dict['spr_TNR']) / const_dict['const_ST']
        MLT = const_dict['const_MLR'] * (self._order_vars_dict['spr_TNR'] - 1)
        MCT = const_dict['const_CRT'] * const_dict['const_CRF']
        MDT = self._order_vars_dict['spr_TCY'] / (self._order_vars_dict['spr_DY'] * const_dict['const_DT'])
        XSST = (const_dict['const_CST'] + MMT + MNT + MUT + const_dict['const_SSA']) / const_dict['const_OEF']
        XST = (MS + MT + MRT + MLT + MCT + MDT) / const_dict['const_OEF']
        self._ost = XSST + XST

        # OCT:
        MCMT2 = self._order_vars_dict['cut_TCL'] / const_dict['const_CV']
        NCM2 = self._order_vars_dict['cut_TCL'] / const_dict['const_CLT']
        MCMTS2 = NCM2 * const_dict['const_CLTS']
        MCT2 = self._order_vars_dict['cut_TCP1'] / const_dict['const_CS']
        MPMT2 = self._order_vars_dict['cut_TCP2'] * const_dict['const_PMT']
        self._oct = (MCMT2 + MCMTS2 + MCT2 + MPMT2 + const_dict['const_CST']) / const_dict['const_OEF']

        self._tdt = self._oct + self._ost

        #print('calculations finished!')

    def get_oct(self):
        return self._oct
    
    def get_ost(self):
        return self._ost
    
    def get_tdt(self):
        return self._tdt

    def __str__(self):
        return ("Sample object:\n"
                "  Name = {0}\n"
                "  Due Date = {1}\n"
                "  Priority = {2}\n"
                "  Total Time = {3}"
                .format(self._ID, self._due_date, self._priority,
                    self._tdt))

#################################

processing = False

class SeniorProject(ProjectGUI.Dialog):
   def OnClose(self, event):
      if not processing:
         self.Destroy()
         exit()

   def OnExit(self, event):
      self.OnClose(event)

   def pause(self, timeout):
      if (timeout > 0):
         loop_count = int(timeout/100)
         remainder = timeout/100 - loop_count
         for count in range(loop_count):
            # yield to allow GUI application to remain responsive while timing
            wx.Yield()
            time.sleep(0.1)
            wx.Yield()
         time.sleep(remainder)

   def md5_file(self, file, blocksize=4096):
      with open(file, "rb") as f:
         file_hash = hashlib.md5()
         for block in iter(lambda: f.read(blocksize), b""):
            file_hash.update(block)
      return file_hash.hexdigest()

   def processFile(self, file):
      self.m_status_message.SetLabel("Processing " + str(file))
      print("Processing " + str(file))
      # processFile currently performs md5 on file
      # replace with desired processing
      self.pause(100)  #artifical pause (to be removed)
      md5 = self.md5_file(file)
      self.m_status_message.SetLabel("md5 of " + str(file) + " = " + str(md5))
      print("Finished. md5 of " + str(file) + " = " + str(md5))
      self.pause(100)  #artifical pause (to be removed)

   def enable_buttons(self, value):
      self.m_exit_button.Enable(value)
      self.m_help_button.Enable(value)
      self.m_save_button.Enable(value)
      #self.m_input_dir.Enable(value)
      self.m_output_dir.Enable(value)
      #self.m_input_extension.Enable(value)
      # change text on Start button to Stop when processing
      if value:
         self.m_start_button.SetLabel("Start")
      else:
         self.m_start_button.SetLabel("Stop")

   """def processDirectory(self, directory, type):
      global processing
      if path.exists(directory):
         self.enable_buttons(False)
         for file in pathlib.Path(directory).glob(type):
            self.processFile(file)
            # if 'Stop' button pressed, exit loop
            if not processing:
               break
      if processing:
         processing = False
         self.m_status_message.SetLabel("Waiting...")
      else:
         self.m_status_message.SetLabel("Stopped...")
      self.enable_buttons(True)"""
######################
# This is where the work needs to be done
   def OnStart(self, event):
      """global processing
      # if not already processing
      if not processing:
         processing = True
         #self.processDirectory(self.m_input_dir.GetPath(),self.m_input_extension.GetValue())
         x = threading.Thread(target=self.processDirectory, args=(self.m_input_dir.GetPath(), self.m_input_extension.GetValue(),), daemon=True)
         x.start()
      else:
         processing = False"""
      cut_file = self.m_input_file.GetPath()
      const_dict = {}
      cut_orders = []

      wb = openpyxl.load_workbook(filename=cut_file, read_only=True, data_only=True)
      
      print(wb.sheetnames)
      # Set worksheet to workbook's active sheet
      ws = wb['constants']
      for row in ws.iter_rows(min_row=2, values_only=True):
          parameters = []
          for cell in row:
              if cell is not None:
                  parameters.append(cell)
          if (len(parameters) >=  3) and (isinstance(parameters[2], float) or (isinstance(parameters[2], int))):
              const_dict["const_" + parameters[0]] = parameters[2]
       
      print(const_dict)
      
      ws = wb['orders']
      for row in ws.iter_rows(min_row=2, values_only=True):
          order_dict = {}
          parameters = []
          for cell in row:
              if cell is not None:
                  parameters.append(cell)
          if (len(parameters) >= 12) and (isinstance(parameters[4], float) or (isinstance(parameters[4], int))):
              order_dict["spr_DY"] = parameters[4]
              order_dict["spr_NM"] = parameters[5]
              order_dict["spr_TNR"] = parameters[6]
              order_dict["spr_TCL"] = parameters[7]
              order_dict["spr_TCY"] = parameters[8]
              order_dict["cut_TCP1"] = parameters[9]
              order_dict["cut_TCP2"] = parameters[10]
              order_dict["cut_TCL"] = parameters[11]
              print(parameters[0], order_dict)
      
              cut_orders.append(CutOrder(parameters[0], parameters[1], parameters[2], order_dict))
      
      print(cut_orders)
      
      for order in cut_orders:
          order.do_calcs(const_dict)
          # print(order._id)
          # print(order.get_oct())
          # print(order.get_ost())
          # print(order.get_tdt())
      
      cut_orders.sort(key=lambda x: (x._due_date, -x._priority, -x._tdt), reverse=False)
      
      namelist = []
      for order in cut_orders:
          namelist.append([order._id, math.floor(order._tdt/60)])
      
      print("resulting schedule:")
      print(namelist)
      
       
      wb.close()
      
      # Create new excel file for ordered list of cut orders
      # Create new workbook
      wb = Workbook()
      # Change sheet to workbook's active sheet
      ws = wb.create_sheet("Ordered Cut List", 0)
        # Set Column headers
      ws['A1'] = 'Order ID'
      ws['B1'] = 'Required Date'
      ws['C1'] = 'Priority'
      ws['D1'] = 'Total Time'
      
      # Go through sorted list of items, setting cell values from CutOrder object parameters
      row_iter = 2
      while row_iter < (len(cut_orders) + 1):
          for order in cut_orders:
              ws['A' + str(row_iter)] = order._id
              ws['B' + str(row_iter)] = order._due_date
              ws['C' + str(row_iter)] = order._priority
              ws['D' + str(row_iter)] = math.floor(order._tdt/60)
              row_iter += 1
      
        # Save to new excel file
      wb.save(self.m_output_dir.GetPath() + '\Ordered Cuts.xlsx')

################

   def OnSave(self, event):
      config = configparser.ConfigParser()
      config.add_section('configuration')
      config.set('configuration', 'output_dir', self.m_output_dir.GetPath())
      #config.set('configuration', 'input_dir', self.m_input_dir.GetPath())
      #config.set('configuration', 'input_extension', self.m_input_extension.GetValue())
      config.set('configuration', 'input_file', self.m_input_file.GetPath())
      with open('settings.ini', 'w') as configfile:
         config.write(configfile)

   def OnHelp(self, event):
      wx.MessageBox("Help for application", "Help", wx.ICON_INFORMATION)

   def OnLoad(self):
      if path.exists('settings.ini'):
         config = configparser.ConfigParser()
         config.read('settings.ini')
         self.m_output_dir.SetPath(config.get('configuration', 'output_dir', fallback=''))
         #self.m_input_dir.SetPath(config.get('configuration', 'input_dir', fallback=''))
         #self.m_input_extension.SetValue(config.get('configuration', 'input_extension', fallback='*.txt'))
         self.m_input_file.SetPath(config.get('configuration', 'input_file', fallback=''))

def main():
      # create a wx app, False stands for no redirection of stdin/stdout
      app = wx.App(False)
      # create an object of wxBacCmd
      frame = SeniorProject(None)
      # load the initial settings
      SeniorProject.OnLoad(frame)
      # show the frame
      frame.Show(True)
      # start the application
      app.MainLoop()

if __name__ == "__main__":
   main()
