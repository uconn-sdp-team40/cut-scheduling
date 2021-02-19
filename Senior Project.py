import wx
import ProjectGUI
import configparser
import pathlib
import time
import hashlib
import threading
from os import path

#############################
import openpyxl
from openpyxl import load_workbook
from openpyxl import Workbook

#Object for each order in Excel file
class CutOrder:
   def __init__(self, name, due_date, priority, tc1, tc2):
      self._cut_name = name
      self._due_date = due_date
      self._priority = int(float(priority))
      self._time_component_1 = int(float(tc1))
      self._time_component_2 = int(float(tc1))
      self._total_time = self._time_component_1 + self._time_component_2

   def __str__(self):
      return ("Sample object:\n"
              "  Name = {0}\n"
              "  Due Date = {1}\n"
              "  Priority = {2}\n"
              "  Total Time = {3}"
              .format(self._cut_name, self._due_date, self._priority,
                      self._total_time))
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
      wb = openpyxl.load_workbook(filename=cut_file, read_only=True)

      print(wb.sheetnames)
      # Set worksheet to workbook's active sheet
      ws = wb.active
      items = []
      for row in ws.iter_rows(min_row=2, values_only=True):
         parameters = []
         for cell in row:
            parameters.append(cell)
         item = CutOrder(*parameters)
         items.append(item)

      # Sort by Due Date, priority, and total time
      items.sort(key=lambda x: (x._due_date, x._priority, -x._total_time), reverse=False)

      for item in items:
         print(item)
         print()

      wb.close()

      # Create new excel file for ordered list of cut orders
      # Create new workbook
      wb = Workbook()
      # Change sheet to workbook's active sheet
      ws = wb.create_sheet("Ordered Cut List", 0)
      # Set Column headers
      ws['A1'] = 'Schedule Number'
      ws['B1'] = 'Cut Name'
      ws['C1'] = 'Required Date'
      ws['D1'] = 'Priority'
      ws['E1'] = 'Total Time'

      # Go through sorted list of items, setting cell values from CutOrder object parameters
      row_iter = 2
      schedule_num = 1
      while row_iter < (len(items) + 1):
         for item in items:
            ws['A' + str(row_iter)] = schedule_num
            ws['B' + str(row_iter)] = item._cut_name
            ws['C' + str(row_iter)] = item._due_date
            ws['D' + str(row_iter)] = item._priority
            ws['E' + str(row_iter)] = item._total_time
            row_iter += 1
            schedule_num += 1

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
