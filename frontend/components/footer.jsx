import React, { Component } from 'react';
import { Link } from "react-router-dom";

export default class Footer extends Component {
  render() {
    return (
      <div className="footer">
        <div>
            <Link to="/">
                <strong>Stats Don't Lie</strong>
            </Link>
            <p>Created by Purab Shah. Data scraped from <a href="https://www.basketball-reference.com/">Basketball Reference</a></p>
        </div>
      </div>
    );
  }
}
