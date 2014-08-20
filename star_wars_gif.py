#!/usr/bin/python

import urwid
import pysrt
from makeGifs import makeGif

choices = [ { 'name': "Star Wars: The Phantom Menace", 'num': 1 },
			{ 'name': "Star Wars: Attack of the Clones", 'num': 2 },
			{ 'name': "Star Wars: Revenge of the Sith", 'num': 3 } ]

sub_files = {   1: 'subs/Star.Wars.Episode.I.srt',
				2: 'subs/Star.Wars.Episode.II.srt',
				3: 'subs/Star.Wars.Episode.III.srt' }

source = 0
index = 0
subtitle = ""

def menu(title, choices):
	body = [urwid.Text(title), urwid.Divider()]
	for c in choices:
		button = urwid.Button(c['name'])
		urwid.connect_signal(button, 'click', item_chosen, c)
		body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
	global source
	response = urwid.Text([u'You chose ', choice['name'], u'\n'])
	source = choice['num']
	done = urwid.Button(u'Ok')
	urwid.connect_signal(done, 'click', search)
	main.original_widget = urwid.Filler(urwid.Pile([response,
		urwid.AttrMap(done, None, focus_map='reversed')]))

def search(button):
	edit = urwid.Edit("Search quotes: ")
	done = urwid.Button(u'Search')
	urwid.connect_signal(done, 'click', find_quotes, edit)
	main.original_widget = urwid.Filler(urwid.Pile([edit,
		urwid.AttrMap(done, None, focus_map='reversed')]))

def find_quotes(button, edit):
	subs = pysrt.open(sub_files[source])
	search = edit.edit_text.lower()

	def seek(item, quote):
		for i in item.split(' '):
			if not i in quote:
				return False
		return True
	matching = [s for s in subs if seek(search, s.text.lower())]

	body = [urwid.Text("Select quote"), urwid.Divider()]
	for m in matching:
		button = urwid.Button(m.text)
		urwid.connect_signal(button, 'click', add_custom_subtitle, subs.index(m))
		body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

def add_custom_subtitle(button, i):
	global index
	index = i
	body = [urwid.Text("Add a custom quote?"), urwid.Divider()]
	yes_button = urwid.Button("Yes")
	urwid.connect_signal(yes_button, 'click', enter_custom_subtitle)
	body.append(urwid.AttrMap(yes_button, None, focus_map='reversed'))
	no_button = urwid.Button("No")
	urwid.connect_signal(no_button, 'click', generate_gif)
	body.append(urwid.AttrMap(no_button, None, focus_map='reversed'))
	main.original_widget = urwid.ListBox(urwid.SimpleFocusListWalker(body))

def enter_custom_subtitle(button):
	subtitle = urwid.Edit("Enter custom subtitle: ")
	done = urwid.Button(u'Submit')
	urwid.connect_signal(done, 'click', generate_gif_with_subtitle, subtitle)
	main.original_widget = urwid.Filler(urwid.Pile([subtitle,
		urwid.AttrMap(done, None, focus_map='reversed')]))

def generate_gif(button):
	raise urwid.ExitMainLoop()

def generate_gif_with_subtitle(button, edit):
	global subtitle
	subtitle = edit.edit_text
	raise urwid.ExitMainLoop()

main = urwid.Padding(menu(u'Movie choice', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
	align='center', width=('relative', 60),
	valign='middle', height=('relative', 60),
	min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
makeGif(source, index, custom_subtitle=subtitle)
