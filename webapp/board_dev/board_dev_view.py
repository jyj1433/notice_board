import os

from flask import Flask, Blueprint, render_template, request, redirect, flash, session, jsonify, send_file, url_for
import math
import config

from werkzeug.utils import secure_filename

import webapp.board_dev.board_devDAO as board_devDAO

bp = Blueprint("board_dev", __name__, url_prefix='/')
dao = board_devDAO.Board_devDAO