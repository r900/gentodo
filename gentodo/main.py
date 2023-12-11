#!/usr/bin/env python
# (c) 2023 Christopher Fore
# This code is licensed under the GPLv3 license (see LICENSE for details)

__version__ = '0.0.5'

import json
import os
import argparse

STORAGE_DIR = os.path.expanduser("~/.local/share/todo")
TODO_FILE = os.path.join(STORAGE_DIR, "todo.json")

class Gentodo:

    def __init__(self):
        self.data = self.read()
        self.longest = self.calc_length()

    def calc_length(self):
        longest = 0

        for todo_id in self.data:
            # Edge case in case someone doesn't put anything in
            if self.data[todo_id]['title'] == None:
                continue
            if len(self.data[todo_id]['title']) > longest:
                longest = len(self.data[todo_id]['title'])
    
        return longest


    def read(self):
        with open(TODO_FILE, "r") as todo:
            return json.load(todo)
    

    def write(self):
        with open(TODO_FILE, "w") as todo:
            json.dump(self.data, todo, indent=4)


def show_todo(args, gentodo):
    '''Shows the items to do'''
    spaces = gentodo.longest + 2

    # Verbose output
    if args.verbose:    
        print("{:<20}│ {:<20}│ Details".format("ID", "Item"))
        print("{}".format("─" * 50))
        for key in gentodo.data:
            print(f"{key:<20}│ {gentodo.data[key]['title']:<20}│ {gentodo.data[key]['details']}")
    else:
        pad_title = f"{{:<{spaces}}}│ Details"
        print(f"{{:<{spaces}}}│ Details".format("Title"))
        print("{}".format("─" * int(48*1.5)))
        for key in gentodo.data:
            pad_string = f"{{:<{spaces}}}| {{}}"
            print(pad_string.format(gentodo.data[key]['title'], gentodo.data[key]['details']))


def add_item(args, gentodo):
    '''Adds an item to the todo list'''
    if os.path.exists(TODO_FILE) and os.path.getsize(TODO_FILE) > 0:
        #data = read_storage()
        newest_id = 0 if len(gentodo.data.keys()) == 0 else int(list(gentodo.data.keys())[-1])
    else:
        data = {}
        newest_id = 0
    
    gentodo.data[newest_id + 1] = { 
        "title": " ".join(args.title),
        "details": " ".join(args.details)
    }

    gentodo.write()
    print(f"Added: {' '.join(args.title)} | {' '.join(args.details)}")


def rm_item(args, gentodo):
    '''Removes an item from the todo list by ID'''
    if os.path.exists(TODO_FILE) and os.path.getsize(TODO_FILE) > 0:
        gentodo.data.pop("{0}".format(args.id))
        gentodo.write()
        

def item_count(args, gentodo):
    '''Tallies up the amount of items in the list'''
        
    remaining = len(gentodo.data.keys())
    print(f"Items remaining: {remaining}")


def edit_item(args, gentodo):
    '''Edits an item entry'''
    gentodo.data[args.id]['title'] = " ".join(args.title)
    gentodo.data[args.id]['details'] = " ".join(args.details)
    
    gentodo.write()


def search_items(args, gentodo):
    print(f"Searching for: {args.term}")
    for key in gentodo.data:
        for val in gentodo.data[key]:
            if args.term in gentodo.data[key][val]:
                print(gentodo.data[key])


def setup_parser():
    '''Sets up the parser and adds arguments'''

    # Main parser
    parser = argparse.ArgumentParser(usage="todo <command> [-h]")
    parser.add_argument('--version', action='version', version='0.0.1')
    parser.add_argument('-v', '--verbose', action='store_true',help="Be descriptive about output (i.e. show item IDs)")
    #parser.add_argument('id')
    parser.set_defaults(func=show_todo)
    
    subparsers = parser.add_subparsers(help='sub-command help', metavar='')
    
    # Parser for adding items
    add_parser = subparsers.add_parser('add', help="Add an item to your todo list", usage="todo add [-h] -t <title> -d <details>")
    add_parser.add_argument('-t', '--title', nargs='+', help="Item to add to your todo list")
    add_parser.add_argument('-d', '--details', nargs='+', help="Add some information to your item")
    add_parser.set_defaults(func=add_item)
    
    # Parser for removing items
    del_parser = subparsers.add_parser('del', help="Remove an item from your todo list", usage="todo rm <id>")
    del_parser.add_argument('id', help="ID to remove from your todo list")
    del_parser.set_defaults(func=rm_item)

    # Parser for counting items
    count_parser = subparsers.add_parser('count', help="Shows your remaining item count")
    count_parser.set_defaults(func=item_count)

    # Parser for editing
    edit_parser = subparsers.add_parser('edit', help="Edit an item by id", usage="todo edit <id> -t <title> -d <details>")
    edit_parser.add_argument('id')
    edit_parser.add_argument('-t', '--title', nargs='+', help="New title")
    edit_parser.add_argument('-d', '--details', nargs='+', help="New details")
    edit_parser.set_defaults(func=edit_item)

    # Parser for searching
    search_parser = subparsers.add_parser('search', help="Search for an item", usage="todo search [term]")
    search_parser.add_argument('term')
    search_parser.set_defaults(func=search_items)

    return parser


def main():
    if not os.path.isdir(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
    gentodo = Gentodo()
    parser = setup_parser()
    #parser.set_defaults(func=gentodo.show_todo)

    #parser_funcs = {
    #    'add': gentodo.add_item,
    #    'del': gentodo.rm_item,
    #    'edit': gentodo.edit_item,
    #    'count': gentodo.item_count,
    #    'search': gentodo.search_items,
    #}

    args = parser.parse_args()
    args.func(args, gentodo)
    #command = args.func.__name__
    #parser.set_defaults(func=gentodo.show_todo)
    #if command in parser_funcs:
    #    print("c")
    #    parser_funcs[command](args)
    #else:
    #    gentodo.show_todo(args)

if __name__ == "__main__":
    main()
