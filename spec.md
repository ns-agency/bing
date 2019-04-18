# Patch 1

## Introduction

You know the drill, fix up some of the bugs you were cracking open for BREAK 2. If you were not able to find all the bugs, see lab 7 for the solutions.

> Note this is only for 6443 students and not extended students

## Deadline 

This is due by midday (12:00) May 1st. 

## Source

https://github.com/ns-agency/bing

There are 2 folders each with 1 site under them, fix the source for both to be secure and pass the provided tests. We will mark your diff but will not run any further tests.

Make sure you check if the repo has been updated whenever you sit down to work on the patch in case there was a fix pushed out.

## Running

In the source code above there is a README.md in the root dir on how to run the site. Because of the complexity of these sites we are providing you with the [docker]("https://www.docker.com/) containers for the sites. As such we require you to install docker. 

> Note if you have trouble running these images locally you can simply clone and run them on a aws/digital ocean box which will work better, simply run it on the box and you can connect the the box via the 8009 and 8010 ports. (you may need to open these ports for aws box's)

## Fixing

There are multiple different ways to patch these programs but as long as you patch it in a way that is justifiable you'll get the marks. We will be reading through your diffs to determine this so try to keep your diff as short as possible. 

If you have any questions / need clarifications you can email the class account or ping the slack channel.

Note you do not have to fix _every_ issue with these sites as some are trivial (i.e removing the client side site that gives you access to a staff api end point), see the tests to get an idea on what we do want you to fix.

## Testing

In the README.md in the root dir there is also instructions on how to run the tests. These rely on the site running on your machine so the tests can connect to it. You may read the source code of the tests to see what each test is looking for.

If you pass all these tests you are set for full marks assuming that your fixes did not simply make the test pass rather then fixing the issue. I.e changeing it from a base 58 to a base 64 does _not_ fix the issue although it will pass the test.

## Files

You will most likely need to edit views.py in each site, although you arn't limited to this if you feel something else needs to change as well.

*Pastebing* : `pastebing/app/pastebing/main/views.py`
*Drive.bing* : `drive.bing/app/bing_drive/main/views.py`

## Submission 

Submit your diff as a patch.

```bash
git diff > z5555555.patch
give cs6443 patch2 z5555555.patch
```