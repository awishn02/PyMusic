SOUNDCLOUD = 0
YOUTUBE = 1
SOUNDCLOUD_CIENT_ID = "cc4c6047b842cbb29c40f65c1855d56e"

$(function(){
  var Feed = Backbone.Model.extend();

  var FeedList = Backbone.Collection.extend({
    model: Feed,
    url: function(){
      search = $("#search-feeds").val()
      if (search != ""){
        return '/feeds.json?search='+search;
      }
      if ($("#feed-list").hasClass('editing')){
        return '/feeds.json?all=1'
      }
      return '/feeds.json';
    }
  });

  var Feeds = new FeedList;

  var FeedView = Backbone.View.extend({
    tagName: "li",
    template: _.template($("#feed-template").html()),
    render: function(){
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    },
    events: {
      "click .view" : "filterByFeed"
    },
    filterByFeed: function(){
      if (!$("#feed-list").hasClass('editing')){
        feed_id = this.$el.find('.view').data('feed_id');
        $("#feed-list li").removeClass('active');
        if (feed_id == Songs.feed_id){
          Songs.feed_id = null
        }else{
          this.$el.addClass('active');
          Songs.feed_id = feed_id;
        }
        Songs.fetch({reset:true});
      }
    }
  });

  var Song = Backbone.Model.extend();

  var SongList = Backbone.Collection.extend({
    model: Song,
    feed_id: null,
    url: function(){
      if (this.feed_id == null){
        return '/songs';
      }else{
        return '/songs?feed_id='+this.feed_id;
      }
    }
  });

  var Songs = new SongList;

  var SongView = Backbone.View.extend({
    tagName: "li",
    template: _.template($("#song-template").html()),
    render: function(){
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    },
    events: {
      "click .view" : "playSong",
      "click .download" : "downloadSong",
      "click .dislike" : "dislikeSong"
    },
    playSong: function(){
      if(player.isLoading == false){
        player.isLoading = true;
        $("#song-list li").removeClass('playing');
        player.curTitle = this.$el.find('p').text();
        $.scrollTo(this.$el.offset().top-40, 600);
        var div = this.$el.find('.view');
        player.curItemView = this;
        var player_id = div.data('player_id');
        var song_id = div.data('song_id');
        player.playSong(song_id, player_id);
        this.$el.addClass('playing');
        $(".play").addClass('active');
      }
    },
    playNext: function(){
      this.$el.removeClass('playing');
      this.$el.next().find('.view').click();
    },
    playPrev: function(){
      this.$el.removeClass('playing');
      this.$el.prev().find('.view').click();
    },
    dislikeSong: function(e){
      e.stopPropagation();
      e.preventDefault();
      var elmt = this.$el;
      var div = this.$el.find('.view');
      var song_id = div.data('id');
      var user_id = $("#edit-feed").data('user_id');
      $.ajax({
        url: "/dislike?user_id="+user_id+"&song_id="+song_id,
        type: "POST",
        success: function(){
          elmt.fadeToggle("fast",function(){
            elmt.remove();
          });
        }
      })
    },
    downloadSong: function(e){
      e.stopPropagation();
      e.preventDefault();
      var div = this.$el.find('.view');
      var player_id = div.data('player_id');
      var song_id = div.data('song_id');
      if(player_id == SOUNDCLOUD){
        $.ajax({
          url: "http://api.soundcloud.com/tracks/"+song_id+".json?client_id="+SOUNDCLOUD_CIENT_ID,
          success:function(r,s,x){
            url = r.permalink_url;
            $.ajax({
              url: "/scdownload?url="+url,
              type: "POST",
              success:function(response, status, xhr){
                var a = document.createElement('a');
                a.setAttribute('href',response);
                filename = response.replace("/static/","");
                a.setAttribute('download', filename);
                a.click();
                a.remove();
              }
            })
          }
        })
      }else if(player_id == YOUTUBE){
        url = "http://www.youtube.com/watch?v="+song_id;
        $.ajax({
          url:'/ytdownload?url='+url,
          type: "POST",
          success:function(response, status, xhr){
            var a = document.createElement('a');
            a.setAttribute('href',response);
            filename = response.replace("/static/","");
            a.setAttribute('download', filename);
            a.click();
            a.remove();
          }
        })
      }
    }
  });

  var AppView = Backbone.View.extend({
    el: $("#song-app"),
    initialize: function(){
      this.listenTo(Songs, 'reset', this.addAll);
      this.listenTo(Feeds, 'reset', this.populateFeedList);
      this.loginAction = "login";
      Feeds.fetch({reset:true});
      Songs.fetch({reset:true});
    },
    events: {
      "click .pause"    : "pause",
      "click .play"     : "play",
      "click .next"     : "next",
      "click .previous" : "previous",
      "click .edit"     : "edit",
      "keyup #search-feeds" : "search",
      "click .bookmark" : "bookmark",
      "click .login"    : "toggleLogin",
      "submit #login"   : "login",
      "click .modal-wrapper.show" : "toggleLogin",
      "click #register" : "toggleRegister"
    },
    addOne: function(song){
      var view = new SongView({model:song});
      this.$("#song-list").append(view.render().el);
    },
    addAll: function(){
      $("#song-list").empty();
      Songs.each(this.addOne);
    },
    addFeed: function(feed){
      var view = new FeedView({model:feed});
      this.$("#feed-list").append(view.render().el);
    },
    pause: function(){
      $(".controls a").removeClass('active');
      $(".pause").addClass('active');
      player.pause();
    },
    play: function(){
      $(".controls a").removeClass('active');
      $(".play").addClass('active');
      player.resume();
    },
    next: function(){
      player.next();
    },
    previous: function(){
      player.previous();
    },
    populateFeedList: function(){
      this.$("#feed-list").empty();
      Feeds.each(this.addFeed);
    },
    edit: function(){
      if($("#search-feeds").hasClass('hidden')){
        $("#search-feeds").removeClass('hidden');
        $("#feed-list").addClass('editing');
        Feeds.fetch({reset:true});
      }else{
        $("#search-feeds").addClass('hidden');
        $("#feed-list").removeClass('editing');
        Feeds.fetch({reset:true});
      }
    },
    search: function(){
      clearTimeout(searchTimer);
      searchTimer = setTimeout(function(){
        Feeds.fetch({reset:true});
      }, 300);
    },
    bookmark: function(e){
      $(e.target).toggleClass('bookmarked');
      var feed_id = $(e.target).parent().parent().data('feed_id');
      var user_id = $("#edit-feed").data('user_id');
      $.ajax({
        url: '/favorite?user_id='+user_id+'&feed_id='+feed_id,
        type: 'POST'
      });
    },
    toggleLogin: function(e){
      $(".login-modal").toggleClass('show');
      $(".modal-wrapper").toggleClass('show');
      $(".content").toggleClass('no-scroll');
      e.preventDefault();
    },
    toggleRegister: function(e){
      if(this.loginAction == "login"){
        this.loginAction = "register";
        $("#register").text('Login');
      }else{
        this.loginAction = "login";
        $("#register").text('Register');
      }
    },
    login: function(e){
      var email = $("#email").val();
      var pass = $("#password").val();
      var remember = $("#remember_me").val();
      var o = this;
      var hold = e;
      if(this.loginAction == "login"){
        url = '/login?email='+email+'&password='+pass+'&remember_me='+remember;
      }else {
        url = '/register?email='+email+'&password='+pass+'&remember_me='+remember
      }
      $.ajax({
        url: url,
        type: 'POST',
        success: function(){
          // o.toggleLogin();
          // Songs.fetch({reset:true});
          // Feeds.fetch({reset:true});
          window.location.reload();
        }
      });
      hold.preventDefault();

    }
  });

  var searchTimer = null;

  var App = new AppView;

  $('.seeker').click(function(e){
    var posX = e.pageX-$(this).offset().left;
    var width = $(this).width();
    var newpos = posX/width;
    player.seek(newpos);
  });

  $(".menu").click(function(){
    $(".songs").toggleClass('active');
    $(".feeds").toggleClass('active');
    $(".navbar").toggleClass('active');
    $("#search-feeds").addClass('hidden');
    $("#feed-list").removeClass('editing');
  })

  player.seeker = $('.seeker');
  player.position = $('.position');

  player.update_seeker = function(){
    curtime = player.ytPlayer.getCurrentTime();
    duration = player.ytPlayer.getDuration();
    player.setSeekPosition(curtime/duration*100);
  }

  window.onfocus = function(){
    player.isActive = true;
  }

  window.onblur = function(){
    player.isActive = false;
  }

});

var curSongItem = null;

JsPlayer = function(){
  SC.initialize({
    client_id: SOUNDCLOUD_CIENT_ID
  });

}
JsPlayer.prototype.ytPlayer = null;
JsPlayer.prototype.setYTPlayer = function(){
  this.ytPlayer = $("#myytplayer");
}
JsPlayer.prototype.playSong = function(song_id, player_id){
  if(Notification.permission === "default"){
    Notification.requestPermission();
  }
  this.stop();
  this.curPlayer = player_id;
  if(player_id == SOUNDCLOUD){
    this.playSC(song_id);
  }else if(player_id == YOUTUBE){
    this.playYT(song_id)
  }
}
JsPlayer.prototype.isActive = true;
JsPlayer.prototype.didSkip = false;
JsPlayer.prototype.curTitle = "";
JsPlayer.prototype.curSound = null;
JsPlayer.prototype.curPlayer = null;
JsPlayer.prototype.curItemView = null;
JsPlayer.prototype.isLoading = false;
JsPlayer.prototype.notify = function(){
  var o = this;
  if(Notification.permission === "granted" && (this.isActive == false || this.didSkip == true)){
    o.didSkip = false;
    var notification = new Notification("PyMusic",{body: o.curTitle})
    notification.onclick = function(){
      o.didSkip = true;
      o.next();
    }
    setTimeout(function(){
      notification.close();
    }, 3000);
  }
}
JsPlayer.prototype.playSC = function(song_id){
  var o = this;
  SC.stream("/tracks/"+song_id, function(sound){
    o.curSound = sound;
    sound.play({
      whileplaying: function(){
        o.isLoading = false;
        width = this.position / this.duration * 100;
        o.setSeekPosition(width);
      },
      onfinish: function(){
        o.next();
      }
    });
  });
}
JsPlayer.prototype.yt_seek_updater = null;
JsPlayer.prototype.playYT = function(song_id){
  this.ytPlayer.loadVideoById(song_id);
  this.isLoading = false;
  this.yt_seek_updater = setInterval(this.update_seeker, 500);
}
JsPlayer.prototype.update_seeker = null;JsPlayer.prototype.seeker = null;
JsPlayer.prototype.seeker
JsPlayer.prototype.position = null;
JsPlayer.prototype.setSeekPosition = function(pos){
  this.position.css('width', pos+'%');
}
JsPlayer.prototype.seek = function(pos){
  this.setSeekPosition(pos*100);
  if(this.curPlayer == SOUNDCLOUD){
    this.curSound.setPosition(pos*this.curSound.duration);
  }else if(this.curPlayer == YOUTUBE){
    this.ytPlayer.seekTo(pos*this.ytPlayer.getDuration());
  }
}
JsPlayer.prototype.stop = function(){
  if(this.curPlayer == SOUNDCLOUD && this.curSound != null){
    this.curSound.stop();
  }else if(this.curPlayer == YOUTUBE){
    this.ytPlayer.stopVideo();
    this.yt_seek_updater = clearInterval(this.yt_seek_updater);
  }
}
JsPlayer.prototype.pause = function(){
  if(this.curPlayer == SOUNDCLOUD && this.curSound != null){
    this.curSound.pause();
  }else if(this.curPlayer == YOUTUBE){
    this.ytPlayer.pauseVideo();
  }
}
JsPlayer.prototype.resume = function(){
  if(this.curPlayer == SOUNDCLOUD && this.curSound != null){
    this.curSound.play();
  }else if(this.curPlayer == YOUTUBE){
    this.ytPlayer.playVideo();
  }
}
JsPlayer.prototype.next = function(){
  this.curItemView.playNext();
  this.notify();
}
JsPlayer.prototype.previous = function(){
  this.curItemView.playPrev();
}

var player = new JsPlayer;
