/**
*  tn menu builder adapted from
 * wpadmin navmenu.js
 */

var tnMenuBuilder;

var tnmb = tnMenuBuilder = {

    options : {
      menuItemDepthPerLevel : 30, // Do not use directly. Use depthToPx and pxToDepth instead.
      globalMaxDepth : 11
    },

    menuList : undefined,  // Set in init.
    targetList : undefined, // Set in init.
    menusChanged : false,
    isRTL: !! ( 'undefined' != typeof isRtl && isRtl ),
    negateIfRTL: ( 'undefined' != typeof isRtl && isRtl ) ? -1 : 1,

    // Functions that run on init.
    __init__ : function() {
      tnmb.menuList = jq('#menu-to-edit');
      tnmb.targetList = tnmb.menuList;

      this.jQueryExtensions();

      if( tnmb.menuList.length )
        this.initSortables();

    },

    jQueryExtensions : function() {
      // jQuery extensions
      jq.fn.extend({
        menuItemDepth : function() {
          var margin = tnmb.isRTL ? this.eq(0).css('margin-right') : this.eq(0).css('margin-left');
          return tnmb.pxToDepth( margin && -1 != margin.indexOf('px') ? margin.slice(0, -2) : 0 );
        },
        updateDepthClass : function(current, prev) {
          return this.each(function(){
            var t = jq(this);
            prev = prev || t.menuItemDepth();
            jq(this).removeClass('menu-item-depth-'+ prev )
              .addClass('menu-item-depth-'+ current );
          });
        },
        shiftDepthClass : function(change) {
          return this.each(function(){
            var t = jq(this),
              depth = t.menuItemDepth();
            jq(this).removeClass('menu-item-depth-'+ depth )
              .addClass('menu-item-depth-'+ (depth + change) );
          });
        },
        childMenuItems : function() {
          var result = jq();
          this.each(function(){
            var t = jq(this), depth = t.menuItemDepth(), next = t.next();
            while( next.length && next.menuItemDepth() > depth ) {
              result = result.add( next );
              next = next.next();
            }
          });
          return result;
        },
        updateParentMenuItemDBId : function() {
          return this.each(function(){
            var item = jq(this),
              input = item.find('.menu-item-data-parent-id'),
              depth = item.menuItemDepth(),
              parent = item.prev();

            if( depth == 0 ) { // Item is on the top level, has no parent
              input.val(0);
            } else { // Find the parent item, and retrieve its object id.
              while( ! parent[0] || ! parent[0].className || -1 == parent[0].className.indexOf('menu-item') || ( parent.menuItemDepth() != depth - 1 ) )
                parent = parent.prev();
              input.val( parent.find('.menu-item-data-db-id').val() );
            }
          });
        },
        hideAdvancedMenuItemFields : function() {
          return this.each(function(){
            var that = jq(this);
            jq('.hide-column-tog').not(':checked').each(function(){
              that.find('.field-' + jq(this).val() ).addClass('hidden-field');
            });
          });
        },
        /**
         * Adds selected menu items to the menu.
         *
         * @param jQuery metabox The metabox jQuery object.
         */
        addSelectedToMenu : function(processMethod) {
          if ( 0 == jq('#menu-to-edit').length ) {
            return false;
          }

          return this.each(function() {
            var t = jq(this), menuItems = {},
              checkboxes = t.find('.tabs-panel-active .categorychecklist li input:checked'),
              re = new RegExp('menu-item\\[(\[^\\]\]*)');

            processMethod = processMethod || tnmb.addMenuItemToBottom;

            // If no items are checked, bail.
            if ( !checkboxes.length )
              return false;

            // Show the ajax spinner
            t.find('img.waiting').show();

            // Retrieve menu item data
            jq(checkboxes).each(function(){
              var t = jq(this),
                listItemDBIDMatch = re.exec( t.attr('name') ),
                listItemDBID = 'undefined' == typeof listItemDBIDMatch[1] ? 0 : parseInt(listItemDBIDMatch[1], 10);
              if ( this.className && -1 != this.className.indexOf('add-to-top') )
                processMethod = tnmb.addMenuItemToTop;
              menuItems[listItemDBID] = t.closest('li').getItemData( 'add-menu-item', listItemDBID );
            });

            // Add the items
            tnmb.addItemToMenu(menuItems, processMethod, function(){
              // Deselect the items and hide the ajax spinner
              checkboxes.removeAttr('checked');
              t.find('img.waiting').hide();
            });
          });
        },
        getItemData : function( itemType, id ) {
          itemType = itemType || 'menu-item';

          var itemData = {}, i,
          fields = [
            'menu-item-db-id',
            'menu-item-object-id',
            'menu-item-object',
            'menu-item-parent-id',
            'menu-item-position',
            'menu-item-type',
            'menu-item-title',
            'menu-item-url',
            'menu-item-description',
            'menu-item-attr-title',
            'menu-item-target',
            'menu-item-classes',
            'menu-item-xfn'
          ];

          if( !id && itemType == 'menu-item' ) {
            id = this.find('.menu-item-data-db-id').val();
          }

          if( !id ) return itemData;

          this.find('input').each(function() {
            var field;
            i = fields.length;
            while ( i-- ) {
              if( itemType == 'menu-item' )
                field = fields[i] + '[' + id + ']';
              else if( itemType == 'add-menu-item' )
                field = 'menu-item[' + id + '][' + fields[i] + ']';

              if (
                this.name &&
                field == this.name
              ) {
                itemData[fields[i]] = this.value;
              }
            }
          });

          return itemData;
        },
        setItemData : function( itemData, itemType, id ) { // Can take a type, such as 'menu-item', or an id.
          itemType = itemType || 'menu-item';

          if( !id && itemType == 'menu-item' ) {
            id = jq('.menu-item-data-db-id', this).val();
          }

          if( !id ) return this;

          this.find('input').each(function() {
            var t = jq(this), field;
            jq.each( itemData, function( attr, val ) {
              if( itemType == 'menu-item' )
                field = attr + '[' + id + ']';
              else if( itemType == 'add-menu-item' )
                field = 'menu-item[' + id + '][' + attr + ']';

              if ( field == t.attr('name') ) {
                t.val( val );
              }
            });
          });
          return this;
        }
      });
    },

    initSortables : function() {
      var currentDepth = 0, originalDepth, minDepth, maxDepth,
        prev, next, prevBottom, nextThreshold, helperHeight, transport,
        menuEdge = tnmb.menuList.offset().left,
        body = jq('body'), maxChildDepth,
        menuMaxDepth = initialMenuMaxDepth();

      // Use the right edge if RTL.
      menuEdge += tnmb.isRTL ? tnmb.menuList.width() : 0;

      tnmb.menuList.sortable({
        handle: '.menu-item-handle',
        placeholder: 'sortable-placeholder',
        start: function(e, ui) {
          var height, width, parent, children, tempHolder;

          // handle placement for rtl orientation
          if ( tnmb.isRTL )
            ui.item[0].style.right = 'auto';

          transport = ui.item.children('.menu-item-transport');

          // Set depths. currentDepth must be set before children are located.
          originalDepth = ui.item.menuItemDepth();
          updateCurrentDepth(ui, originalDepth);

          // Attach child elements to parent
          // Skip the placeholder
          parent = ( ui.item.next()[0] == ui.placeholder[0] ) ? ui.item.next() : ui.item;
          children = parent.childMenuItems();
          transport.append( children );

          // Update the height of the placeholder to match the moving item.
          height = transport.outerHeight();
          // If there are children, account for distance between top of children and parent
          height += ( height > 0 ) ? (ui.placeholder.css('margin-top').slice(0, -2) * 1) : 0;
          height += ui.helper.outerHeight();
          helperHeight = height;
          height -= 2; // Subtract 2 for borders
          ui.placeholder.height(height);

          // Update the width of the placeholder to match the moving item.
          maxChildDepth = originalDepth;
          children.each(function(){
            var depth = jq(this).menuItemDepth();
            maxChildDepth = (depth > maxChildDepth) ? depth : maxChildDepth;
          });
          width = ui.helper.find('.menu-item-handle').outerWidth(); // Get original width
          width += tnmb.depthToPx(maxChildDepth - originalDepth); // Account for children
          width -= 2; // Subtract 2 for borders
          ui.placeholder.width(width);

          // Update the list of menu items.
          tempHolder = ui.placeholder.next();
          tempHolder.css( 'margin-top', helperHeight + 'px' ); // Set the margin to absorb the placeholder
          ui.placeholder.detach(); // detach or jQuery UI will think the placeholder is a menu item
          jq(this).sortable( "refresh" ); // The children aren't sortable. We should let jQ UI know.
          ui.item.after( ui.placeholder ); // reattach the placeholder.
          tempHolder.css('margin-top', 0); // reset the margin

          // Now that the element is complete, we can update...
          updateSharedVars(ui);
        },
        stop: function(e, ui) {
          var children, depthChange = currentDepth - originalDepth;

          // Return child elements to the list
          children = transport.children().insertAfter(ui.item);

          // Update depth classes
          if( depthChange != 0 ) {
            ui.item.updateDepthClass( currentDepth );
            children.shiftDepthClass( depthChange );
            updateMenuMaxDepth( depthChange );
          }
          // Register a change
          tnmb.registerChange();
          // Update the item data.
          ui.item.updateParentMenuItemDBId();

          // address sortable's incorrectly-calculated top in opera
          ui.item[0].style.top = 0;

          // handle drop placement for rtl orientation
          if ( tnmb.isRTL ) {
            ui.item[0].style.left = 'auto';
            ui.item[0].style.right = 0;
          }

          // The width of the tab bar might have changed. Just in case.
          //tnmb.refreshMenuTabs( true );
        },
        change: function(e, ui) {
          // Make sure the placeholder is inside the menu.
          // Otherwise fix it, or we're in trouble.
          if( ! ui.placeholder.parent().hasClass('menu') )
            (prev.length) ? prev.after( ui.placeholder ) : tnmb.menuList.prepend( ui.placeholder );

          updateSharedVars(ui);
        },
        sort: function(e, ui) {
          var offset = ui.helper.offset(),
            edge = tnmb.isRTL ? offset.left + ui.helper.width() : offset.left,
            depth = tnmb.negateIfRTL * tnmb.pxToDepth( edge - menuEdge );
          // Check and correct if depth is not within range.
          // Also, if the dragged element is dragged upwards over
          // an item, shift the placeholder to a child position.
          if ( depth > maxDepth || offset.top < prevBottom ) depth = maxDepth;
          else if ( depth < minDepth ) depth = minDepth;

          if( depth != currentDepth )
            updateCurrentDepth(ui, depth);

          // If we overlap the next element, manually shift downwards
          if( nextThreshold && offset.top + helperHeight > nextThreshold ) {
            next.after( ui.placeholder );
            updateSharedVars( ui );
            jq(this).sortable( "refreshPositions" );
          }
        }
      });

      function updateSharedVars(ui) {
        var depth;

        prev = ui.placeholder.prev();
        next = ui.placeholder.next();

        // Make sure we don't select the moving item.
        if( prev[0] == ui.item[0] ) prev = prev.prev();
        if( next[0] == ui.item[0] ) next = next.next();

        prevBottom = (prev.length) ? prev.offset().top + prev.height() : 0;
        nextThreshold = (next.length) ? next.offset().top + next.height() / 3 : 0;
        minDepth = (next.length) ? next.menuItemDepth() : 0;

        if( prev.length )
          maxDepth = ( (depth = prev.menuItemDepth() + 1) > tnmb.options.globalMaxDepth ) ? tnmb.options.globalMaxDepth : depth;
        else
          maxDepth = 0;
      }

      function updateCurrentDepth(ui, depth) {
        ui.placeholder.updateDepthClass( depth, currentDepth );
        currentDepth = depth;
      }

      function initialMenuMaxDepth() {
        if( ! body[0].className ) return 0;
        var match = body[0].className.match(/menu-max-depth-(\d+)/);
        return match && match[1] ? parseInt(match[1]) : 0;
      }

      function updateMenuMaxDepth( depthChange ) {
        var depth, newDepth = menuMaxDepth;
        if ( depthChange === 0 ) {
          return;
        } else if ( depthChange > 0 ) {
          depth = maxChildDepth + depthChange;
          if( depth > menuMaxDepth )
            newDepth = depth;
        } else if ( depthChange < 0 && maxChildDepth == menuMaxDepth ) {
          while( ! jq('.menu-item-depth-' + newDepth, tnmb.menuList).length && newDepth > 0 )
            newDepth--;
        }
        // Update the depth class.
        body.removeClass( 'menu-max-depth-' + menuMaxDepth ).addClass( 'menu-max-depth-' + newDepth );
        menuMaxDepth = newDepth;
      }
    },

    updateQuickSearchResults : function(input) {
      var panel, params,
      minSearchLength = 2,
      q = input.val();

      if( q.length < minSearchLength ) return;

      panel = input.parents('.tabs-panel');
      params = {
        'action': 'menu-quick-search',
        'response-format': 'markup',
        'menu': jq('#menu').val(),
        'menu-settings-column-nonce': jq('#menu-settings-column-nonce').val(),
        'q': q,
        'type': input.attr('name')
      };

      jq('img.waiting', panel).show();

      jq.post( ajaxurl, params, function(menuMarkup) {
        tnmb.processQuickSearchQueryResponse(menuMarkup, params, panel);
      });
    },

    addCustomLink : function( processMethod ) {
      var url = jq('#custom-menu-item-url').val(),
        label = jq('#custom-menu-item-name').val();

      processMethod = processMethod || tnmb.addMenuItemToBottom;

      if ( '' == url || 'http://' == url )
        return false;

      // Show the ajax spinner
      jq('.customlinkdiv img.waiting').show();
      this.addLinkToMenu( url, label, processMethod, function() {
        // Remove the ajax spinner
        jq('.customlinkdiv img.waiting').hide();
        // Set custom link form back to defaults
        jq('#custom-menu-item-name').val('').blur();
        jq('#custom-menu-item-url').val('http://');
      });
    },

    addLinkToMenu : function(url, label, processMethod, callback) {
      processMethod = processMethod || tnmb.addMenuItemToBottom;
      callback = callback || function(){};

      tnmb.addItemToMenu({
        '-1': {
          'menu-item-type': 'custom',
          'menu-item-url': url,
          'menu-item-title': label
        }
      }, processMethod, callback);
    },

    addItemToMenu : function(menuItem, processMethod, callback) {
      var menu = jq('#menu').val(),
        nonce = jq('#menu-settings-column-nonce').val();

      processMethod = processMethod || function(){};
      callback = callback || function(){};

      params = {
        'action': 'add-menu-item',
        'menu': menu,
        'menu-settings-column-nonce': nonce,
        'menu-item': menuItem
      };

      jq.post( ajaxurl, params, function(menuMarkup) {
        var ins = jq('#menu-instructions');
        processMethod(menuMarkup, params);
        if( ! ins.hasClass('menu-instructions-inactive') && ins.siblings().length )
          ins.addClass('menu-instructions-inactive');
        callback();
      });
    },

    /**
     * Process the add menu item request response into menu list item.
     *
     * @param string menuMarkup The text server response of menu item markup.
     * @param object req The request arguments.
     */
    addMenuItemToBottom : function( menuMarkup, req ) {
      jq(menuMarkup).hideAdvancedMenuItemFields().appendTo( tnmb.targetList );
    },

    addMenuItemToTop : function( menuMarkup, req ) {
      jq(menuMarkup).hideAdvancedMenuItemFields().prependTo( tnmb.targetList );
    },

    registerChange : function() {
      tnmb.menusChanged = true;
    },

    eventOnClickEditLink : function(clickedEl) {
      var settings, item,
      matchedSection = /#(.*)jq/.exec(clickedEl.href);
      if ( matchedSection && matchedSection[1] ) {
        settings = jq('#'+matchedSection[1]);
        item = settings.parent();
        if( 0 != item.length ) {
          if( item.hasClass('menu-item-edit-inactive') ) {
            if( ! settings.data('menu-item-data') ) {
              settings.data( 'menu-item-data', settings.getItemData() );
            }
            settings.slideDown('fast');
            item.removeClass('menu-item-edit-inactive')
              .addClass('menu-item-edit-active');
          } else {
            settings.slideUp('fast');
            item.removeClass('menu-item-edit-active')
              .addClass('menu-item-edit-inactive');
          }
          return false;
        }
      }
    },

    eventOnClickCancelLink : function(clickedEl) {
      var settings = jq(clickedEl).closest('.menu-item-settings');
      settings.setItemData( settings.data('menu-item-data') );
      return false;
    },

    eventOnClickMenuSave : function(clickedEl) {
      var locs = '',
      menuName = jq('#menu-name'),
      menuNameVal = menuName.val();
      // Cancel and warn if invalid menu name
      if( !menuNameVal || menuNameVal == menuName.attr('title') || !menuNameVal.replace(/\s+/, '') ) {
        menuName.parent().addClass('form-invalid');
        return false;
      }
      // Copy menu theme locations
      jq('#nav-menu-theme-locations select').each(function() {
        locs += '<input type="hidden" name="' + this.name + '" value="' + jq(this).val() + '" />';
      });
      jq('#update-nav-menu').append( locs );
      // Update menu item position data
      tnmb.menuList.find('.menu-item-data-position').val( function(index) { return index + 1; } );
      window.onbeforeunload = null;

      return true;
    },

    eventOnClickMenuDelete : function(clickedEl) {
      // Delete warning AYS
      if ( confirm( navMenuL10n.warnDeleteMenu ) ) {
        window.onbeforeunload = null;
        return true;
      }
      return false;
    },

    eventOnClickMenuItemDelete : function(clickedEl) {
      var itemID = parseInt(clickedEl.id.replace('delete-', ''), 10);
      tnmb.removeMenuItem( jq('#menu-item-' + itemID) );
      tnmb.registerChange();
      return false;
    },

    /**
     * Process the quick search response into a search result
     *
     * @param string resp The server response to the query.
     * @param object req The request arguments.
     * @param jQuery panel The tabs panel we're searching in.
     */
    processQuickSearchQueryResponse : function(resp, req, panel) {
      var matched, newID,
      takenIDs = {},
      form = document.getElementById('nav-menu-meta'),
      pattern = new RegExp('menu-item\\[(\[^\\]\]*)', 'g'),
      jqitems = jq('<div>').html(resp).find('li'),
      jqitem;

      if( ! jqitems.length ) {
        jq('.categorychecklist', panel).html( '<li><p>' + navMenuL10n.noResultsFound + '</p></li>' );
        jq('img.waiting', panel).hide();
        return;
      }

      jqitems.each(function(){
        jqitem = jq(this);

        // make a unique DB ID number
        matched = pattern.exec(jqitem.html());

        if ( matched && matched[1] ) {
          newID = matched[1];
          while( form.elements['menu-item[' + newID + '][menu-item-type]'] || takenIDs[ newID ] ) {
            newID--;
          }

          takenIDs[newID] = true;
          if ( newID != matched[1] ) {
            jqitem.html( jqitem.html().replace(new RegExp(
              'menu-item\\[' + matched[1] + '\\]', 'g'),
              'menu-item[' + newID + ']'
            ) );
          }
        }
      });

      jq('.categorychecklist', panel).html( jqitems );
      jq('img.waiting', panel).hide();
    },

    removeMenuItem : function(el) {
      var children = el.childMenuItems();

      el.addClass('deleting').animate({
          opacity : 0,
          height: 0
        }, 350, function() {
          var ins = jq('#menu-instructions');
          el.remove();
          children.shiftDepthClass(-1).updateParentMenuItemDBId();
          if( ! ins.siblings().length )
            ins.removeClass('menu-instructions-inactive');
        });
    },

    depthToPx : function(depth) {
      return depth * tnmb.options.menuItemDepthPerLevel;
    },

    pxToDepth : function(px) {
      return Math.floor(px / tnmb.options.menuItemDepthPerLevel);
    }

};


jq(document).ready(function(){ tnMenuBuilder.__init__(); });


