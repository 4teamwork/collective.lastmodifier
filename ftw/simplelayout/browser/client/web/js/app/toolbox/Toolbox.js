define(["app/simplelayout/Element", "jsrender", "jquery-path"], function(Element) {

  "use strict";

  var Toolbox = function(options) {

    if (!(this instanceof Toolbox)) {
      throw new TypeError("Toolbox constructor cannot be called as a function.");
    }

    var template = $.templates(
    /*eslint no-multi-str: 0 */
    "<div id='sl-toolbox' class='sl-toolbox'> \
      <div> \
        <a class='sl-toolbox-header blocks'> \
          <i></i> \
        </a> \
          <div class='sl-toolbox-blocks'> \
            {{for blocks}} \
              <a class='sl-toolbox-block {{:contentType}}' data-type='{{:contentType}}' data-form-url='{{:formUrl}}'> \
                <i class='icon-{{:contentType}}'></i> \
                <span class='description'>{{:title}}</span> \
              </a> \
            {{/for}} \
          </div> \
          {{if canChangeLayout}} \
            <a class='sl-toolbox-header layouts'> \
              <i></i> \
            </a> \
            <div class='sl-toolbox-layouts'> \
              {{props layouts}} \
                <a class='sl-toolbox-layout' data-columns='{{>prop}}'>{{>prop}} \
                  <span class='description'>{{>prop}}{{>#parent.parent.data.labels.labelColumnPostfix}}</span> \
                </a> \
              {{/props}} \
            </div> \
          {{/if}} \
        </div> \
      </div>");

    Element.call(this, template);

    this.options = $.extend({
      layouts: [1, 2, 4],
      blocks: [],
      labels: {},
      layoutActions: {}
    }, options || {});

    this.create({
      blocks: this.options.blocks,
      layouts: this.options.layouts,
      labels: this.options.labels,
      canChangeLayout: this.options.canChangeLayout
    });

    var blockObjects = {};
    $.each(this.options.blocks, function(idx, block) {
      blockObjects[block.contentType] = block;
    });

    this.options.blocks = blockObjects;

    this.attachTo = function(target) { target.append(this.element); };

    this.blocksEnabled = function(state) { $(".sl-toolbox-blocks", this.element).toggleClass("disabled", !state); };

    /* Patch for registring beforeStart event */
    var oldMouseStart = $.ui.draggable.prototype._mouseStart;
    $.ui.draggable.prototype._mouseStart = function (event, overrideHandle, noActivation) {
        this._trigger("beforeStart", event, this._uiHash());
        oldMouseStart.apply(this, [event, overrideHandle, noActivation]);
    };

    this.triggerHint = function(addable, target, animationOptions) {
      animationOptions = $.extend({
        time: 500,
        easing: "easeInOutQuad"
      }, animationOptions);
      var path = {
        start: {
          x: addable.offset().left - addable.offset().left,
          y: addable.offset().top,
          angle: 70
        },
        end: {
          x: -target.offset().left - (target.width() / 2) + (addable.width() / 2),
          y: target.offset().top,
          angle: 290
        }
      };
      /*eslint new-cap: 0 */
      var bezier = new $.path.bezier(path);
      var clone = addable.clone().insertAfter(addable);
      clone.css("position", "absolute").css("z-index", "1");
      clone.animate({ path: bezier }, animationOptions.time, animationOptions.easing, function() { clone.css("z-index", "auto").addClass("hintDropped"); });
      setTimeout(function() { clone.remove(); }, animationOptions.time + 300);
    };

  };

  Element.call(Toolbox.prototype);

  return Toolbox;

});
