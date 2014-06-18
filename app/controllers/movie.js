import Ember from 'ember';

export default Ember.ObjectController.extend({
  isEditing: false,

  actions: {
    newGoof: function() {
      this.set('isEditing', true);
    },

    doneEditing: function() {
      var desc = this.get('newDescription') || '',
          minutes = this.get('newMinutes') || '',
          seconds = this.get('newSeconds') || '',
          movie = this.get('content');

      if(!!desc && !!minutes && !!seconds) {
        var goof = this.store.createRecord('goof', {
          description: desc,
          minutes: minutes,
          seconds: seconds,
          movie: movie
        });

        this.send('cancelEditing');

        goof.save().then(function(goof) {
          movie.get('goofs').pushObject(goof);
          return movie;
        });
      }
    },

    cancelEditing: function() {
      this.setProperties({
        newDescription: '',
        newMinutes: '',
        newSeconds: '',
        isEditing: false
      });
    }
  }
});
