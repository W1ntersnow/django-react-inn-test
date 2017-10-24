import Dropdown from 'react-dropdown'
import React, { Component } from 'react'

class DropDown extends Component {

  render(){
      return(
         <div>
         <p>FORMAT: row_number. user_id / username / inn / cash </p>
         <Dropdown options={this.props.data.map(
            function(user, i){
               return <div>{i}. {user.id} / {user.username} / {user.inn} / {user.cash}</div>;
            })} onChange={this.props.handleUser}/>
         </div>
      );
  }
}

export default DropDown