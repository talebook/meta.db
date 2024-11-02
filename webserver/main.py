#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.options

import click
import os 
import logging

import models
import handlers


tornado.options.define("host", default="", type=str, help=_("The host address on which to listen"))
tornado.options.define("port", default=8080, type=int, help=_("The port on which to listen."))
tornado.options.define("log-file", default=os.environ.get('LOG_FILENAME', None), type=str, help=_("Path to logging"))
tornado.options.define("mongo-addr", default=os.environ.get('MONGO_ADDR', None), type=str, help=_("db address"))
tornado.options.define("max-upload-size", default=os.environ.get('MAX_UPLOAD_SIZE', "100M"), type=str, help=_("max upload size"))


def get_upload_size(max_upload_size):
    n = 1
    s = max_upload_size.lower().strip()
    if s.endswith("k") or s.endswith("kb"):
        n = 1024
        s = s.split("k")[0]
    elif s.endswith("m") or s.endswith("mb"):
        n = 1024 * 1024
        s = s.split("m")[0]
    elif s.endswith("g") or s.endswith("gb"):
        n = 1024 * 1024 * 1024
        s = s.split("g")[0]
    s = s.strip()
    return int(s) * n


def setup_logging(log_filename=None):
    logger = logging.getLogger()
    logging.info("Init logging with [%s]" % log_filename)

    if log_filename:
        h = logging.handlers.RotatingFileHandler(log_filename, mode='a', maxBytes=100 * 1024 * 1024, backupCount=10)
        h.setLevel(logging.DEBUG)
        h.setFormatter(tornado.log.LogFormatter())
        logger.addHandler(h)


def make_app():
    return tornado.web.Application([
        (r"/api/register", handlers.RegisterHandler),
        (r"/api/reset_password", handlers.ResetPasswordHandler),
        (r"/api/search_books", handlers.SearchBooksHandler),
        (r"/api/upload_file", handlers.UploadFileHandler),
    ])


def main(listen, mongo_addr, timeout, verbose):
    tornado.options.parse_command_line()
    args = tornado.options.options
    setup_logging(args.log_file)

    models.init()
    app = make_app()

    http_server = tornado.httpserver.HTTPServer(app, xheaders=True, max_buffer_size=get_upload_size(args.max_upload_size))
    http_server.listen(args.port, args.host)
    logging.info(f"Server started at http://{args.host}:{args.port}")

    # 创建一个定时任务，每隔60秒执行一次
    # periodic_callback = tornado.ioloop.PeriodicCallback(IPDB.clear_cache, 3600*1000)
    # periodic_callback.start()

    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__))
    sys.exit(main())