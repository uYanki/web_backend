#include "widget.h"

#include "QDebug"

#include "server.h"

server server;

Widget::Widget(QWidget* parent)
    : QWidget(parent) {

    // 注： 服务器地址留空代表根目录

    /* 取文件列表 */
    file_info* arr = nullptr; // 文件列表缓冲数组
    size_t     cnt = server.list("", &arr); // 数组元素个数
    for (size_t i = 0; i < cnt; ++i) {
        // do something at here
        qDebug() << arr[i].name << ", " << arr[i].path;
    }

    /* 获取文件 */
    if(cnt>0){
        file_info f = arr[cnt - 1];
        if (f.type == true) {  // 类型 false=dir true=file
            server.fench(f.path, "f:/661.txt");
            // server.fench(f.path,"./662.txt");
        }
    }


    /* 上传文件 */
    server.upload("", "f:/3.txt");
    server.upload("666", "f:/2.txt");

    /* 释放内存 */
    if (arr) {
        delete arr;
        arr = nullptr;
    }
}

Widget::~Widget() {
}
