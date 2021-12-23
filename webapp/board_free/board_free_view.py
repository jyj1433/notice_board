import os

from flask import Flask, Blueprint, render_template, request, redirect, flash, session, jsonify, send_file, url_for
import math
import config

from werkzeug.utils import secure_filename

import webapp.board_free.board_freeDAO as board_freeDAO

bp = Blueprint("board_free", __name__, url_prefix='/')
dao = board_freeDAO.Board_freeDAO