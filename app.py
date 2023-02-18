import argparse
from random import shuffle, choice
from math import ceil
import sys
import time

def read_in_emails() -> list:
  emails = []
  try:
    emails = input("Paste all the emails: ").split('\n')
  except:
    print("Couldn't parse emails")
  return emails

def remove_dupes(emails: list) -> list:
  unduped = []
  dupes = 0
  [unduped.append(x.strip()) for x in emails if x.strip() not in unduped]
  dupes = len(emails) - len(unduped)
  return unduped, dupes

def randomize_list(emails: list, times: int) -> list:

  for x in range(0, times):
    shuffle(emails)
    print(".", end="", flush=True)
    time.sleep(0.01)
  print()
  return emails

def pick_winners(emails: list, picks: int) -> list:
  winners = []
  for x in range(0, picks):
    winner = choice(emails)
    winners.append(winner)
    emails.pop(emails.index(winner))
  
  return winners

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--file', dest="emails", help="A file with all the emails")
  parser.add_argument('-s', '--shuffle', default=5, dest="shuffle", type=int, help="The amount of times to shuffle the list")
  parser.add_argument('-w', '--winners', default=1, dest="winners", type=int, help="The number of winners to pick")
  parser.add_argument('-p', '--public', default=False, dest="public", action="store_true", help="Hide output")
  args = parser.parse_args()

  print(f"Shuffling {args.shuffle} times and picking {args.winners} winners")
  if args.emails:
    # parse emails
    with open(args.emails, 'r') as f:
      emails = f.readlines()
  else:
    emails = read_in_emails()


  print("Removing duplicates")
  emails, dupes = remove_dupes(emails)
  if args.winners > len(emails):
    print("More winners than entrants, reducing to half the list")
    args.winners = ceil(len(emails) / 2)
    print(args.winners)
  print(f"Shuffling list {args.shuffle} times")
  emails = randomize_list(emails, args.shuffle)
  print(f"Picking {args.winners} winners")
  winners = pick_winners(emails, args.winners)
  print(f"There were {len(emails) + len(winners)} entries and {len(winners)} winners picked. Also {dupes} dupes")

  if args.public: 
    for w in winners:
      print("\t{}".format("x"*len(w)))
    with open(f"{args.emails.split('.')[0]}_winners.txt", 'w') as f:
      for l in winners:
        f.write(f"{l}\n")
  else:
    for w in winners:
      print("\t{}".format(w))
  return 0

if __name__ == "__main__":
  sys.exit(main())