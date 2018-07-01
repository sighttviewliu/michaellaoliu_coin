// Copyright (c) 2011-2017 The Michaellaoliu Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef MICHAELLAOLIU_QT_UTILITYDIALOG_H
#define MICHAELLAOLIU_QT_UTILITYDIALOG_H

#include <QDialog>
#include <QObject>

class MichaellaoliuGUI;

namespace Ui {
    class HelpMessageDialog;
}

/** "Help message" dialog box */
class HelpMessageDialog : public QDialog
{
    Q_OBJECT

public:
    explicit HelpMessageDialog(QWidget *parent, bool about);
    ~HelpMessageDialog();

    void printToConsole();
    void showOrPrint();

private:
    Ui::HelpMessageDialog *ui;
    QString text;

private Q_SLOTS:
    void on_okButton_accepted();
};


/** "Shutdown" window */
class ShutdownWindow : public QWidget
{
    Q_OBJECT

public:
    explicit ShutdownWindow(QWidget *parent=0, Qt::WindowFlags f=0);
    static QWidget *showShutdownWindow(MichaellaoliuGUI *window);

protected:
    void closeEvent(QCloseEvent *event);
};

#endif // MICHAELLAOLIU_QT_UTILITYDIALOG_H
