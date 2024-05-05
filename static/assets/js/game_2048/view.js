var View = (function () {

    var tileContainer = $('.tile-container')[0];
    var scoreContainer = $('.score-container')[0];
    var scoreDom = $('.score-container .score')[0];
    var scoreAddition = $('.score-addition')[0];
    var bestDom = $('.best-container .score')[0];
    var failureContainer = $('.failure-container')[0];
    var winningContainer = $('.winning-container')[0];

    class View {
        constructor() {
        }
        setup() {
            failureContainer.classList.remove('action');
            winningContainer.classList.remove('action');
            this.updateScore(data.score);
            this.updateBest();
        }
        restart() {
            tileContainer.innerHTML = "";
        }
        resize() {
            var _this = this;
            data.cell.forEach(function (el, index) {
                var tile = _this.getTile(index);
                if (!tile) return;
                var pos = _this.getPos(indexToPos(index));
                _this.setPos(tile, pos);
            });
        }
        failure() {
            failureContainer.classList.add('action');
        }
        winning() {
            winningContainer.classList.add('action');
        }
        restoreTile() {
            var _this = this;
            data.cell.forEach(function (el, index) {
                if (el.val !== 0) {
                    _this.appear(index);
                }
            });
        }
        addScoreAnimation(score) {
            if (!score) return;
            scoreAddition.innerHTML = '+' + score;
            scoreAddition.classList.add('action');
            setTimeout(function () {
                scoreAddition.classList.remove('action');
            }, 500);
        }
        updateScore(score) {
            scoreDom.innerHTML = data.score;
            this.addScoreAnimation(score);
        }
        updateBest() {
            bestDom.innerHTML = data.best;
        }
        setInfo(elem, pos, index) {
            elem.style.left = pos.left + 'px';
            elem.style.top = pos.top + 'px';
            elem.setAttribute('data-index', index);
        }
        getTile(index) {
            return $(`.tile[data-index='${index}']`)[0];
        }
        getPos(pos) {
            var gridCell = $(`.grid-row:nth-child(${pos.y + 1}) .grid-cell:nth-child(${pos.x + 1})`)[0];
            return {
                left: gridCell.offsetLeft,
                top: gridCell.offsetTop,
            };
        }
        setPos(elem, pos) {
            elem.style.left = pos.left + 'px';
            elem.style.top = pos.top + 'px';
        }
        createTileHTML(obj) {
            var tile = document.createElement('div');
            tile.className = obj.classNames;
            tile.innerHTML = obj.val;
            tile.setAttribute('data-index', obj.index);
            tile.setAttribute('data-val', obj.val);
            this.setPos(tile, obj.pos);
            return tile;
        }
        appear(index) {
            var last = data.cell[index];
            var pos = this.getPos(indexToPos(index));
            var newTile = this.createTileHTML({
                val: last.val,
                pos: pos,
                index: index,
                classNames: " tile new-tile",
            });
            tileContainer.appendChild(newTile);
        }
        remove(index) {
            var tile = this.getTile(index);
            tile.parentElement.removeChild(tile);
        }
        move(old_index, index) {
            var tile = this.getTile(old_index);
            var pos = this.getPos(indexToPos(index));
            this.setInfo(tile, pos, index);
        }
        updateVal(index) {
            var tile = this.getTile(index);
            var val = data.cell[index].val;
            tile.setAttribute('data-val', val);
            tile.innerHTML = val;
            tile.classList.add('addition');
            setTimeout(function () {
                tile.classList.remove('addition');
                tile.classList.remove('new-tile');
            }, 300);
        }
    }


    return View;

})();