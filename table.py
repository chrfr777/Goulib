# -*- coding: utf-8 -*-
"""
=====
Table
=====
:Author: Philippe Guglielmetti <philippe.guglielmetti@bobstgroup.com>
:Date: $Date: 2012-04-05$
:Revision: $Revision: 7056 $
:Description: reads a .csv (Excel) file and manipulates it as a table


Code Documentation
==================
"""

import csv, itertools, operator, string
from datetime import datetime

class Table(list):
    def __init__(self, filename=None, titles=[], init=[]):
        """inits a table either from data or csv file"""
        list.__init__(self, init)
        self.titles=titles
        if filename:
            self.read_csv(filename,len(self.titles)==0)
        
    def read_csv(self, filename, titleline=True):
        """appends a .csv file to the table"""
        reader = csv.reader(open(filename, 'rb'), dialect='excel', delimiter=';')
        if titleline:
            self.titles=reader.next()
        for row in reader:
            line=[]
            for x in row:
                try:
                    x=float(x) if '.' in x else int(x)
                except:
                    if x=='': x=None
                line.append(x)
            self.append(line)
            
    def write_csv(self,filename):
        writer=csv.writer(open(filename, 'wb'), dialect='excel', delimiter=';')
        if self.titles: writer.writerow(self.titles)
        for line in self:
            writer.writerow(line)

    def _i(self,by):
        '''column index'''
        if isinstance(by, basestring):
            return self.titles.index(by)
        return by
    
    def col(self,by):
        '''return column'''
        return [row[self._i(by)] for row in self]
    
    def set(self,row,col,value):
        if row>=len(self): 
            self.extend([list()]*(1+row-len(self)))
        if col>=len(self[row]):
            self[row].extend([None]*(1+col-len(self[row])))
        self[row][col]=value
    
    def setcol(self,by,val,i=0):
        '''set column'''
        for v in val:
            self.set(i,self._i(by),v)
            i+=1
    def addcol(self,title,val,i=0):
        '''add column to the right'''
        col=len(self.titles)
        self.titles.append(title)
        for v in val:
            self.set(i,col,v)
            i+=1
            
    def sort(self,by,reverse=False):
        '''sort by column'''
        i=self._i(by)
        if isinstance(i, int):
            list.sort(self,key=lambda x:x[i],reverse=reverse)
        else:
            list.sort(i,reverse=reverse)
            
    def groupby(self,by):
        '''dictionary of subtables grouped by a column'''
        i=self._i(by)
        self.sort(i)
        t=self.titles[:i]+self.titles[i+1:]
        res={}
        for k, g in itertools.groupby(self, key=lambda x:x[i]):
            res[k]=Table([a[:i]+a[i+1:] for a in list(g)])
            res[k].titles=t
        return res
    
    def applyf(self,by,f):
        '''apply a function to a column'''
        i=self._i(by)
        for row in self:
            row[i]=f(row[i])
            
    def to_datetime(self,by,fmt='%d.%m.%Y'):
        '''convert a column to datetime'''
        self.applyf(by,lambda x:datetime.strptime(x,fmt))
        
    def to_date(self,by,fmt='%d.%m.%Y'):
        '''convert a column to date'''
        self.to_datetime(by,fmt)
        self.applyf(by,lambda x:x.date())
            
    def __str__(self):
        res=''
        if self.titles:
            res+=str(self.titles)+'\n'
        for line in self:
            res+=str(line)+'\n'
        return res