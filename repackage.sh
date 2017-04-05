#!/bin/bash
rm -f *.zip; find . -not -path './.git*' -not -path '.' -not -name '*.pyc' -not -name '*.zip' -not -name 'repackage.sh' -print | zip netrunnerSlackBot.zip -@
