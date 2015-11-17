(function(global, $) {

  "use strict";

  var init = function() {

    var target = $("body");

    var baseUrl = $("body").data("base-url") ? $("body").data("base-url") + "/" : $("base").attr("href");

    var isUploading = function() { return global["xhr_" + $(".main-uploader").attr("id")]._filesInProgress > 0; };

    var initializeColorbox = function() {
      if($(".colorboxLink").length > 0) {
        if (typeof global.ftwColorboxInitialize !== "undefined" && $.isFunction(global.ftwColorboxInitialize)) {
          global.ftwColorboxInitialize();
        }
      }
    };

    var options = $.extend({
      canChangeLayout: false,
      canEdit: false,
      endpoints: {
        toolbox: baseUrl + "sl-toolbox-view",
        state: baseUrl + "sl-ajax-save-state-view"
      }
    }, $(".sl-simplelayout").data("slSettings"));

    if (!options.canEdit) { return false; }

    var deleteOverlay = new global.FormOverlay({cssclass: "overlay-delete"});
    var editOverlay = new global.FormOverlay();
    var uploadOverlay = new global.FormOverlay({ disableClose: isUploading });
    var addOverlay = new global.FormOverlay();
    var toolbox;
    var simplelayout;

    var loadComponents = function(callback) {
      $.get(options.endpoints.toolbox).done(function(data, textStatus, request) {
        var contentType = request.getResponseHeader("Content-Type");
        if (contentType.indexOf("application/json") < 0) {
          throw new Error("Bad response [content-type: " + contentType + "]");
        }
        callback(data);
      });
    };

    var saveState = function() {
      var state = {};
      $(".sl-simplelayout").each(function(manIdx, manager) {
        state[manager.id] = [];
        $(".sl-layout", manager).each(function(layIdx, layout) {
          state[manager.id][layIdx] = {};
          state[manager.id][layIdx].cols = [];
          $(".sl-column", layout).each(function(colIdx, column) {
            state[manager.id][layIdx].cols[colIdx] = { blocks: [] };
            $(".sl-block", column).each(function(bloIdx, block) {
              state[manager.id][layIdx].cols[colIdx].blocks[bloIdx] = { uid: $(block).data().represents };
            });
          });
        });
      });
      $.post(options.endpoints.state, {
        data: JSON.stringify(state),
        _authenticator: $('input[name="_authenticator"]').val()
      });
    };

    loadComponents(function(settings) {

      settings = $.extend(settings, options);

      toolbox = new global.Toolbox(settings);
      toolbox.attachTo(target);

      simplelayout = new global.Simplelayout({toolbox: toolbox, editLayouts: settings.canChangeLayout });

      simplelayout.on("blockInserted", function(block) {
        var layout = block.parent;
        if(layout.hasBlocks()) {
          layout.toolbar.disable("delete");
        }
        if(block.type) {
          addOverlay.load(toolbox.options.blocks[block.type].formUrl);
        }
        addOverlay.onSubmit(function(data) {
          block.represents = data.uid;
          block.data({ represents: data.uid, url: data.url });
          block.content(data.content);
          block.commit();
          saveState();
          this.close();
        });
        addOverlay.onCancel(function() {
          if(!block.committed) {
            block.remove().delete();
          }
        });
      });

      simplelayout.restore(target);

      simplelayout.on("blockDeleted", function(block) {
        var layout = block.parent;
        if(!layout.hasBlocks()) {
          layout.toolbar.enable("delete");
        }
      });

      simplelayout.on("layoutInserted", function(layout) {
        layout.commit();
        toolbox.blocksEnabled(true);
        saveState();
      });

      simplelayout.on("layoutDeleted", function(layout) {
        if(!layout.parent.hasLayouts()) {
          toolbox.blocksEnabled(false);
        }
        saveState();
      });

      simplelayout.on("blockMoved", function() { saveState(); });

      simplelayout.on("beforeBlockMoved", function(beforeBlock) {
        simplelayout.on("blockMoved", function(block) {
          var beforeLayout = beforeBlock.parent;
          var currentLayout = block.parent;
          if(beforeLayout.hasBlocks()) {
            beforeLayout.toolbar.disable("delete");
          } else {
            beforeLayout.toolbar.enable("delete");
          }
          if(currentLayout.hasBlocks()) {
            currentLayout.toolbar.disable("delete");
          } else {
            currentLayout.toolbar.enable("delete");
          }
        });
      });

      simplelayout.on("layoutMoved", function() { saveState(); });

      simplelayout.on("blockReplaced", function() { $(document).trigger("blockContentReplaced", arguments); });

    });

    $(global.document).on("click", ".sl-layout .delete", function() {
      var layout = $(this).parents(".sl-layout").data().object;
      if(!layout.hasBlocks()) {
        layout.remove().delete();
      }
    });

    $(global.document).on("click", ".sl-block .delete", function(event) {
      event.preventDefault();
      var block = $(this).parents(".sl-block").data().object;
      deleteOverlay.load($(this).attr("href"), { data: JSON.stringify({ block: block.represents }) });
      deleteOverlay.onSubmit(function() {
        if(block.committed) {
          block.remove().delete();
        }
        saveState();
        this.close();
      });
    });

    $(global.document).on("click", ".sl-block .edit", function(event) {
      event.preventDefault();
      var block = $(this).parents(".sl-block").data().object;
      editOverlay.load($(this).attr("href"), {"data": JSON.stringify({ "block": block.represents })});
      editOverlay.onSubmit(function(data) {
        block.content(data.content);
        initializeColorbox();
        this.close();
      });
    });

    $(global.document).on("click", ".sl-block .redirect", function(event) {
      event.preventDefault();
      var block = $(this).parents(".sl-block").data().object;
      window.location.href = block.data().url + $(this).attr("href");
    });

    $(global.document).on("click", ".server-action", function(event) {
      event.preventDefault();
      var block = $(this).parents(".sl-block").data().object;
      var payLoad = {};
      var action = $(this);
      payLoad.uid = block.represents;
      $.extend(payLoad, action.data());
      var configRequest = $.post(action.attr("href"), {"data": JSON.stringify(payLoad)});
      configRequest.done(function(blockContent) {
        block.content(blockContent);
      });
    });

    $(global.document).on("click", ".sl-block .upload", function(event) {
      event.preventDefault();
      var block = $(this).parents(".sl-block").data().object;
      uploadOverlay.load($(this).attr("href"), {"data": JSON.stringify({ "block": block.represents })}, function(){
        var self = this;
        global.Browser.onUploadComplete = function(){ return; };
        self.element.on("click", "#button-upload-done", function(uploadEvent) {
          uploadEvent.preventDefault();
          self.onFormCancel.call(self);
        });

      });
      uploadOverlay.onCancel(function(){
        var payLoad = {};
        var action = $(this);
        payLoad.uid = block.represents;
        $.extend(payLoad, action.data());
        var configRequest = $.post("./sl-ajax-reload-block-view", {"data": JSON.stringify(payLoad)});
        configRequest.done(function(blockContent) {
          block.content(blockContent);
          initializeColorbox();
        });
      });
    });

  };

  $(init);

}(window, jQuery));
