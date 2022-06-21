#ifndef server_H
#define server_H

#include "widget.h"

#include "QDebug"

#include "QString"

#include "QNetworkAccessManager"
#include "QNetworkReply"
#include "QNetworkRequest"
#include "QtNetwork"

const QString server_address  = "http://uykweb.xicp.io"; // "http://127.0.0.1:5000";
const QString api_fench_file  = server_address + "/api/get_file/";    // http.get
const QString api_upload_file = server_address + "/api/oper_disk/";  // http.post
const QString api_list_dir    = server_address + "/api/oper_disk/";  // http.get

struct file_info {
    bool    type;  // false=dir true=file
    QString name;
    QString path;
};

class server : public QObject {
public:
    server();
    ~server();

private:
    QNetworkAccessManager* manager;

public:
    // 服务器路径留空代表根目录
    bool   fench(const QString server_filepath /*服务器路径*/, const QString local_filepath /*本地路径*/);
    bool   upload(const QString server_filepath /*服务器路径*/, const QString local_filepath /*本地路径*/);
    size_t list(const QString server_dirpath /*服务器路径*/, file_info** buffer /*路径缓冲数组*/);
};

#endif  // server_H
