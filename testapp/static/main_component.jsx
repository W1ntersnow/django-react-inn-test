import React, { Component } from 'react'
import DropDown from './dropdown.jsx'

class MainComponent extends Component {

  constructor(props) {
      super(props);
      this.state = {
          data: [],
          all_inns: [],
          current_user_id: null,
          current_user: null,
          current_cash: null,
          users_inn: [],
          cash: null,
          updated: null,
      };
      this.handleUser = this.handleUser.bind(this);
      this.handleUsersInn = this.handleUsersInn.bind(this);
      this.handleCash = this.handleCash.bind(this);
      this.handleButton = this.handleButton.bind(this);
  }

  async loadData() {
      this.setState({
          data: await fetch("/api/").then(response =>response.json())
      })
  }

  async firstLoad() {
      this.setState({
          data: await fetch("/api/").then(response =>response.json())
      })
      for (var i = 0; i < this.state.data.length; i++ ){
          this.state.all_inns.push(this.state.data[i].inn)
      }
  }

  componentDidMount() {
      this.firstLoad();
  }

  async update() {
      if (this.state.value !== null ||  this.state.value !== '') {
          var url = "/api/"+this.state.current_user_id+"/"
      } else {
          var url = "/api/"
      }
      const formData = new FormData();
      formData.append('username', this.state.current_user);
      formData.append('cash', this.state.cash);
      formData.append('users_inn', this.state.users_inn);
      this.setState({
          updated: await fetch(url, {
                                      method: 'PUT',
                                      body: formData,
                                    }).then(response =>response.json())
      })
      this.loadData();
  }

  handleUser(val) {
      this.state.current_user_id = parseInt(this.state.data[val.value.props.children[0]].id);
      this.state.current_user = parseInt(this.state.data[val.value.props.children[0]].username);
      this.state.current_cash = parseInt(this.state.data[val.value.props.children[0]].cash);
  }

  handleUsersInn(val) {
      if (val.target.value.split(",").length > 0) {
          this.state.users_inn = val.target.value.split(",");
      }
  }

  handleCash(val) {
      this.state.cash = parseInt(val.target.value)
  }

  handleButton (val) {
      const all_inns = this.state.all_inns
      var is_correct_inns = this.state.users_inn.every(
         function(val) {
            return all_inns.indexOf(parseInt(val)) >= 0;
         }
      )
      if (this.state.users_inn.length < 1) {
          alert('inn count: '.concat(this.state.users_inn.length))
      } else if (this.state.current_cash < this.state.cash) {
          alert('user has only: '.concat(this.state.current_cash))
      } else if (!(this.state.cash > 0)){
          alert('enter correct sum: '.concat(this.state.cash))
      } else if (!is_correct_inns) {
          alert('wrong inns: '.concat(this.state.users_inn))
      } else if (this.state.current_user == null) {
          alert('select user: '.concat(this.state.cash))
      } else {
          this.update();
      }
  }

  render(){
      return(
        <div >
        <DropDown data={this.state.data} handleUser={this.handleUser} />

        <p>enter user_inn for transfer:</p>
        <input onChange={this.handleUsersInn} />

        <p>enter cash for transfer:</p>
        <input onChange={this.handleCash} />

        <br/>
        <button onClick={this.handleButton}>press</button>
        </div>
      );
  }
}

export default MainComponent