# This Python file uses the following encoding: utf-8
from HTMLParser import HTMLParser
import logging

class State:
  START = 0
  BOARD = 1
  TOP = 2
  FLAVOURS = 3
  FLAVOUR = 4
  BOTTOM = 5

class Shop:
  NONE = 0
  DANVER = 1
  DELILA = 2
  DAVIS = 3

class FlavourParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.state = State.START
    self.shop = Shop.NONE
    self.danver_flavours = []
    self.delila_flavours = []
    self.davis_flavours = []
    self.current_flavour = None

  def find_attr(self, attrs, name):
    for attr in attrs:
      if attr[0] == name:
        return attr[1]
    return None

  def handle_starttag(self, tag, attrs):
    if tag == 'img':
      if self.state == State.TOP:
        title = self.find_attr(attrs, 'title')
        if title.find('Danver') >= 0:
          self.shop = Shop.DANVER
        if title.find('Delila') >= 0:
          self.shop = Shop.DELILA
        if title.find('Davis') >= 0:
          self.shop = Shop.DAVIS
    if tag == 'div':
      if self.state == State.START:
        id = self.find_attr(attrs, 'id')
        if id == 'flavourboards':
          self.state = State.BOARD
      elif self.state == State.BOARD:
        clazz = self.find_attr(attrs, 'class')
        if clazz == 'top':
          self.state = State.TOP
        elif clazz == 'flavoursofday':
          self.state = State.FLAVOURS
        elif clazz == 'bottom':
          self.state = State.BOTTOM
      elif self.state == State.FLAVOURS:
        clazz = self.find_attr(attrs, 'class')
        if clazz == 'flavourofday':
          self.state = State.FLAVOUR

  def handle_endtag(self, tag):
    if tag == 'div':
      if self.state == State.BOARD:
        self.state = State.START
      elif self.state == State.TOP:
        self.state = State.BOARD
      elif self.state == State.FLAVOURS:
        self.state = State.BOARD
      elif self.state == State.FLAVOUR:
        if self.shop == Shop.NONE:
          logging.error('Found a flavour without a shop :(')
        elif self.shop == Shop.DANVER:
          self.danver_flavours.append(self.current_flavour)
        elif self.shop == Shop.DAVIS:
          self.davis_flavours.append(self.current_flavour)
        elif self.shop == Shop.DELILA:
          self.delila_flavours.append(self.current_flavour)
        self.current_flavour = None
        self.state = State.FLAVOURS
      elif self.state == State.BOTTOM:
        self.state = State.BOARD

  def handle_data(self, data):
    if self.state == State.FLAVOUR:
      if not self.current_flavour:
        self.current_flavour = data
      else:
        self.current_flavour = self.current_flavour + ' ' + data
