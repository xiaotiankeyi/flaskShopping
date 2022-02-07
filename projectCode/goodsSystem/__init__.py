from flask import Blueprint


goodsSystem = Blueprint('gSystem', __name__, url_prefix='/goods')

from projectCode.goodsSystem import goods, goodsify, goodslist