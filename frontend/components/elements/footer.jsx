import React from 'react';
import { Link } from "react-router-dom";

export default function Footer(props) {
  return (
    <div className="footer is-flexed">
      <div>
          <Link to="/">
              <strong>Stats Don't Lie</strong>
          </Link>
          <p>Created by Purab Shah. Data scraped from <a href="https://www.basketball-reference.com/">Basketball Reference</a></p>
      </div>
      <div className="personal-links">
        <a href="https://github.com/purabshah8">
          <i className="fab fa-github fa-2x"></i>
        </a>
        <a href="http://purab-shah.com">
          <i class="fas fa-laptop-code fa-2x"></i>
        </a>
        <a href="http://www.linkedin.com/in/purab-shah-987717b5/">
          <i className="fab fa-linkedin-in fa-2x"></i>
        </a>
      </div>
    </div>
  );
}
