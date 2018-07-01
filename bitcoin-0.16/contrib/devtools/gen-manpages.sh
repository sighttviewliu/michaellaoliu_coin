#!/bin/bash

TOPDIR=${TOPDIR:-$(git rev-parse --show-toplevel)}
SRCDIR=${SRCDIR:-$TOPDIR/src}
MANDIR=${MANDIR:-$TOPDIR/doc/man}

MICHAELLAOLIUD=${MICHAELLAOLIUD:-$SRCDIR/michaellaoliud}
MICHAELLAOLIUCLI=${MICHAELLAOLIUCLI:-$SRCDIR/michaellaoliu-cli}
MICHAELLAOLIUTX=${MICHAELLAOLIUTX:-$SRCDIR/michaellaoliu-tx}
MICHAELLAOLIUQT=${MICHAELLAOLIUQT:-$SRCDIR/qt/michaellaoliu-qt}

[ ! -x $MICHAELLAOLIUD ] && echo "$MICHAELLAOLIUD not found or not executable." && exit 1

# The autodetected version git tag can screw up manpage output a little bit
MLLVER=($($MICHAELLAOLIUCLI --version | head -n1 | awk -F'[ -]' '{ print $6, $7 }'))

# Create a footer file with copyright content.
# This gets autodetected fine for michaellaoliud if --version-string is not set,
# but has different outcomes for michaellaoliu-qt and michaellaoliu-cli.
echo "[COPYRIGHT]" > footer.h2m
$MICHAELLAOLIUD --version | sed -n '1!p' >> footer.h2m

for cmd in $MICHAELLAOLIUD $MICHAELLAOLIUCLI $MICHAELLAOLIUTX $MICHAELLAOLIUQT; do
  cmdname="${cmd##*/}"
  help2man -N --version-string=${MLLVER[0]} --include=footer.h2m -o ${MANDIR}/${cmdname}.1 ${cmd}
  sed -i "s/\\\-${MLLVER[1]}//g" ${MANDIR}/${cmdname}.1
done

rm -f footer.h2m
