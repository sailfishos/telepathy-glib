#!/bin/sh

cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<testdefinition version="1.0">
    <suite name="telepathy-glib-tests">
        <description>Telepathy Glib tests</description>
        <set name="telepathy-glib-C-tests">
EOF

for testcase in $(cat tests/tpglib-tests.list)
do
    attributes="name=\"$testcase\""
    insignificant=`grep "^$testcase" tests/INSIGNIFICANT || true`
    if test -n "$insignificant"
    then
        continue
        attributes="$attributes insignificant=\"true\""
    fi
    cat <<EOF
        <case $attributes>
            <step>/opt/tests/telepathy-glib/$testcase</step>
        </case>
EOF
done

cat <<EOF
        </set>
        <set name="telepathy-glib-dbus-tests">
EOF

for testcase in $(cat tests/dbus/tpglib-dbus-tests.list)
do
    attributes="name=\"$testcase\""
    insignificant=`grep "^$testcase" tests/INSIGNIFICANT || true`
    if test -n "$insignificant"
    then
        continue
        attributes="$attributes insignificant=\"true\""
    fi
    cat <<EOF
        <case $attributes>
            <step>/opt/tests/telepathy-glib/run-test.sh $testcase</step>
        </case>
EOF
done

cat <<EOF
        </set>
    </suite>
</testdefinition>
EOF
