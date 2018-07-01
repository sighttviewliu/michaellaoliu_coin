// Copyright (c) 2011-2014 The Michaellaoliu Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef MICHAELLAOLIU_QT_MICHAELLAOLIUADDRESSVALIDATOR_H
#define MICHAELLAOLIU_QT_MICHAELLAOLIUADDRESSVALIDATOR_H

#include <QValidator>

/** Base58 entry widget validator, checks for valid characters and
 * removes some whitespace.
 */
class MichaellaoliuAddressEntryValidator : public QValidator
{
    Q_OBJECT

public:
    explicit MichaellaoliuAddressEntryValidator(QObject *parent);

    State validate(QString &input, int &pos) const;
};

/** Michaellaoliu address widget validator, checks for a valid michaellaoliu address.
 */
class MichaellaoliuAddressCheckValidator : public QValidator
{
    Q_OBJECT

public:
    explicit MichaellaoliuAddressCheckValidator(QObject *parent);

    State validate(QString &input, int &pos) const;
};

#endif // MICHAELLAOLIU_QT_MICHAELLAOLIUADDRESSVALIDATOR_H
