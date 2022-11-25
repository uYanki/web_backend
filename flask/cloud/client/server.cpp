#include "server.h"

#include "QDebug"

#include "QJsonDocument"

server::server() {
    manager = new QNetworkAccessManager();
}

server::~server() {
    delete manager;
}

bool server::fench(const QString server_filepath, const QString local_filepath) {
    QNetworkRequest request = QNetworkRequest(QUrl(api_fench_file + server_filepath));  // 设置URL
    request.setHeader(QNetworkRequest::UserAgentHeader, QVariant("Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"));

    QEventLoop     eventLoop;                         // 用于信号阻塞
    QNetworkReply* respones = manager->get(request);  // 发起请求
    connect(respones, SIGNAL(finished()), &eventLoop, SLOT(quit()));
    eventLoop.exec();

    if (respones->error() == QNetworkReply::NoError) {
        QByteArray responseByte = respones->readAll();
        QFile      file(local_filepath);
        if (file.open(QFile::ReadWrite)) {
            file.write(responseByte, responseByte.length());
            return true;
        }
        qDebug() << "when saving file occurs error";
    }

    QVariant statusCode = respones->attribute(QNetworkRequest::HttpStatusCodeAttribute);  // 状态码
    qDebug("http.error:%d,%d", statusCode.toInt(), (int)respones->error());
    qDebug() << respones->errorString();

    return false;
}

bool server::upload(const QString server_dirpath, const QString local_filepath) {

    if (local_filepath == "") return false;

    QFile file(local_filepath);
    if (!file.open(QFile::ReadOnly)) {
        qDebug() << "when reading file occurs error";
        return false;
    }

    QNetworkRequest request;
    request.setUrl(QUrl(api_upload_file + server_dirpath));

    QHttpPart filePart; // 模拟浏览器上传文件
    QFileInfo info(local_filepath);
    QString   header = QString("form-data; name=\"file\";filename=\"%1\"").arg(info.fileName());
    filePart.setHeader(QNetworkRequest::ContentDispositionHeader, QVariant(header));
    filePart.setBodyDevice(&file);

    QHttpMultiPart multiPart(QHttpMultiPart::FormDataType);
    multiPart.append(filePart);

    QEventLoop     eventLoop;
    QNetworkReply* respones = manager->post(request, &multiPart);  // 发起请求
    connect(respones, SIGNAL(finished()), &eventLoop, SLOT(quit()));
    eventLoop.exec();

    if (respones->error() != QNetworkReply::NoError) {
        QVariant statusCode = respones->attribute(QNetworkRequest::HttpStatusCodeAttribute);  // 状态码
        qDebug("http.error:%d,%d", statusCode.toInt(), (int)respones->error());
        qDebug() << respones->errorString();
        return 0;
    }

    QByteArray bytes = respones->readAll();
    qDebug() << QString(bytes);  // 输出服务器返回的结果

    return true;
}

size_t server::list(const QString server_dirpath, file_info** buffer) {
    QNetworkRequest request = QNetworkRequest(QUrl(api_list_dir + server_dirpath));  // 设置URL
    request.setHeader(QNetworkRequest::UserAgentHeader, QVariant("Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"));

    QEventLoop     eventLoop;
    QNetworkReply* respones = manager->get(request);  // 发起请求
    connect(respones, SIGNAL(finished()), &eventLoop, SLOT(quit()));
    eventLoop.exec();

    if (respones->error() != QNetworkReply::NoError) {
        QVariant statusCode = respones->attribute(QNetworkRequest::HttpStatusCodeAttribute);  // 状态码
        qDebug("http.error:%d,%d", statusCode.toInt(), (int)respones->error());
        qDebug() << respones->errorString();
        return 0;
    }

    QByteArray responseByte = respones->readAll();
    // qDebug() << responseByte;
    QJsonParseError json_error;
    QJsonDocument   document = QJsonDocument::fromJson(responseByte, &json_error);
    if (json_error.error == QJsonParseError::NoError) {
        // processing data
        if (document.isObject()) {
            const QJsonObject obj   = document.object();
            const QJsonArray  dirs  = obj.value("dirs").toArray();
            const QJsonArray  files = obj.value("files").toArray();
            size_t            cnt   = dirs.count() + files.count();
            if (cnt == 0) return 0;
            size_t     index = 0;
            file_info* infos = new file_info[cnt];
            // json to array
            for (auto i = dirs.constBegin(); i != dirs.constEnd(); ++i, ++index) {
                QJsonObject dir   = i->toObject();
                infos[index].type = false;
                infos[index].name = dir.value("name").toString();
                infos[index].path = dir.value("path").toString();
            }
            for (auto i = files.constBegin(); i != files.constEnd(); ++i, ++index) {
                QJsonObject file  = i->toObject();
                infos[index].type = true;
                infos[index].name = file.value("name").toString();
                infos[index].path = file.value("path").toString();
            }
            *buffer = infos;
            return cnt;
        }
    }

    return 0;
}
