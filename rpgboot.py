#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import os, sys

slug = sys.argv[1]
title = sys.argv[2]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_loader = FileSystemLoader(BASE_DIR + '/templates')
env = Environment(
  block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
  loader=file_loader
)

print(BASE_DIR)

CURRENT_DIR = os.getcwd()
PROJECT_DIR = CURRENT_DIR + '/' + slug

os.mkdir(PROJECT_DIR)
os.mkdir(PROJECT_DIR + '/manuscript')
os.mkdir(PROJECT_DIR + '/images')

filenames = [
  '.editorconfig',
  '.gitignore',
  'gamebook.cls',
]

for filename in filenames:
  template = env.get_template(filename + '.jinja')
  output = template.render()
  with open(PROJECT_DIR + '/' + filename, 'w') as file:
    file.write(output)

chapters = [
  'Introduction',
  'Character Creation',
  'Combat',
  'Gameplay',
]

template = env.get_template('chapter.tex.jinja')

chapterslugs = []

for chapter in chapters:
  chaptertitle = chapter
  chapterslug = chaptertitle.lower().replace(' ', '-')
  chapterslugs.append(chapterslug)

  output = template.render(chaptertitle=chaptertitle)
  with open(PROJECT_DIR + '/manuscript/' + chapterslug + '.tex', 'w') as file:
    file.write(output)

template = env.get_template('credits.tex.jinja')
output = template.render(title=title)
with open(PROJECT_DIR + '/manuscript/credits.tex', 'w') as file:
  file.write(output)

template = env.get_template('game.tex.jinja')
output = template.render(title=title, slug=slug, chapters=chapterslugs)
with open(PROJECT_DIR + '/' + slug + '.tex', 'w') as file:
  file.write(output)

template = env.get_template('build.sh.jinja')
output = template.render(slug=slug)
with open(PROJECT_DIR + '/build.sh', 'w') as file:
  file.write(output)
