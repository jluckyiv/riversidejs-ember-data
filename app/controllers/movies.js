import Ember from 'ember';

export default Ember.ArrayController.extend({
  isEditing: false,

  actions: {
    newMovie: function() {
      this.set('isEditing', true);
    },

    doneEditing: function() {
      var title = this.get('newTitle') || '',
          year = this.get('newYear') || '',
          director = this.get('newDirector') || '';

      if(!!title && !!year && !!director) {
        var movie = this.store.createRecord('movie', {
          title: title,
          year: year,
          director: director
        });

        this.send('cancelEditing');
        movie.save();
      }
    },

    cancelEditing: function() {
      this.setProperties({
        newTitle: '',
        newYear: '',
        newDirector: '',
        isEditing: false
      });
    }
  },

  searchTitle: '',
  searchFilter: function() {
    var regex = new RegExp(this.get('searchTitle'), 'gi');
    return this.filter(function(movie) {
      return movie.get('title').match(regex);
    });
  }.property('searchTitle', 'model.@each.title')
});
