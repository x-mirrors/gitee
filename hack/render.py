#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author by me@xiexianbin.cn
# function: render README.md/github workflows by template.
# date 2023-07-30

import argparse
import os
import subprocess

from jinja2 import Template

CURRENT_PATH = os.getcwd()

TABLE_HEADERS = [
  'Source',
  'Target',
  'Sync Account',
  'Repo Count',
  'Status']

parser = argparse.ArgumentParser(description='Render README.md/github workflows')
parser.add_argument('--readme', '-r', help='render readme', action=argparse.BooleanOptionalAction,
                    default=False, type=bool)
parser.add_argument('--workflows', '-w', help='render workflows', action=argparse.BooleanOptionalAction,
                    default=False, type=bool)
args = parser.parse_args()


def bash(command: str, force=False, debug=False):
  args = ['bash', '-c', command]

  subp = subprocess.Popen(args, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
  stdout, stderr = subp.communicate()
  code = subp.poll()
  if debug:
    print(f"Run bash: {command}, ret is {code}, stderr is {stderr}")

  if not stdout and not stderr:
    print(f"Run bash: {command}, ret is {code}")

  if force:
    return code, stdout, stderr
  return code


class Render(object):
  def __init__(self):
    self.readme_tpl_path = os.path.join(CURRENT_PATH, 'README.md.tpl')
    self.workflow_tpl_path = os.path.join(CURRENT_PATH, 'sync.yml.tpl')
    self.readme_out_path = os.path.join(CURRENT_PATH, '../README.md')
    self.workflows_base_path = os.path.join(CURRENT_PATH, '../.github/workflows')
    self.sync_conf_path = os.path.join(CURRENT_PATH, 'sync.txt')

  def load_sync_conf(self):
    result = dict()
    with open(self.sync_conf_path, 'r') as f:
      lines = f.readlines()
      for line in lines:
        if line.startswith('#'):
          continue
        line = line.replace('\n', '')
        src, dest = line.split(' ')
        result[src] = dest
    return result

  def get_repo_count(self, name):
    return '-'

  def _get_cron(self, action):
    return action[True]['schedule'][0]['cron']

  def render(self, tpl_path, out_path, info):
    with open(tpl_path, 'r') as in_file, open(out_path, 'w') as out_file:
      tpl = Template(in_file.read())
      out_file.write(tpl.render(info))

  def readme(self):
    mk_lines = []
    mk_lines.append(f"|{'|'.join(TABLE_HEADERS)}|")
    mk_lines.append(f"|{'|'.join([':---' for _ in range(len(TABLE_HEADERS))])}|")

    orgs = self.load_sync_conf()
    target_lines = []
    for src, dest in orgs.items():
      target_lines.append({
        'source': f'[github.com/{src}](https://github.com/{src})',
        'target': f'[gitee.com/{dest}](https://gitee.com/{dest})',
        'sync_account': '-',
        'repo_count': self.get_repo_count(src),
        'status': f'[![github.com/{src}](https://github.com/x-mirrors/gitee/actions/workflows/{src}.yml/badge.svg)](https://github.com/x-mirrors/gitee/actions/workflows/{src}.yml)',
      })

      print(f'## {src} Mirror\n')
      print(f'- sync from https://github.com/{src} by [x-mirrors/gitee](https://github.com/x-mirrors/gitee)')
      print(f'- 其他同步需求：发送邮件到 `me@xiexianbin.cn` 或在 https://github.com/x-mirrors/gitee/ 提交 `issue`\n')

    target_lines = sorted(target_lines, key=lambda x: x['source'])
    for i in target_lines:
      mk_lines.append(
        f"|{'|'.join([i['source'], i['target'], i['sync_account'], str(i['repo_count']), i['status']])}|")

    mk_raw = '\n'.join(mk_lines)
    self.render(self.readme_tpl_path, self.readme_out_path, {'mk_raw': mk_raw})

  def workflows(self):
    orgs = self.load_sync_conf()
    for src, dest in orgs.items():
      out_path = f'{self.workflows_base_path}/{src}.yml'
      self.render(
        self.workflow_tpl_path,
        out_path,
        {'github_org': src, 'gitee_org': dest})


if __name__ == '__main__':
  try:
    if args.readme:
      Render().readme()
    elif args.workflows:
      Render().workflows()
    else:
      parser.print_help()
  except Exception as e:
    print(e)
    raise
