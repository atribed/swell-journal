module.exports = {
  /**
   * Formats UTC string date to EST
   */
  formatD3DateEST: function(date) {
    var formattedDate = new Date(date);
    formattedDate.setHours(formattedDate.getHours() - 5);

    return formattedDate;
  }
}
