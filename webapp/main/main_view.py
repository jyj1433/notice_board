from flask import Flask, Blueprint, render_template, request, redirect, flash, session, jsonify, send_file, url_for
import math
import config

import webapp.main.mainDAO as mainDAO

bp = Blueprint("main", __name__, url_prefix='/')
dao = mainDAO.MainDAO