import { Component } from "react";
import Help from "../img/help-desk.png";
import disease from "../img/disease.png";
import fertile from "../img/fertile.png";

class CardBar extends Component {
  render() {
    return (
      <section className="body__section py-10">
        <div className="grid place-items-center mt-5">
          <p className="text-3xl font-bold text-center text-gray-900 uppercase mb-2">
            Features that are provided
          </p>
          
        </div>
        <div className="grid place-items-center mt-14 mb-20">
          <div className="inline-flex space-x-36 items-center justify-end">
            <div className="w-1/4 h-full">
              <div className="inline-flex flex-col space-y-6 items-center justify-end flex-1 h-full pl-9 pr-8 pt-8 pb-11 bg-white border rounded border-black border-opacity-10">
                <img className="w-1/5 h-12 rounded-lg" src={Help} alt="help" />
                <p className="w-56 h-7 text-lg font-semibold text-gray-900 text-center">
                  24*7 AI call assistance
                </p>
                <p className="opacity-70 w-56 h-1/5 text-base text-center">
                  Providing solutions through calls
                </p>
              </div>
            </div>
            <div className="w-1/4 h-full">
              <div className="inline-flex flex-col space-y-6 items-center justify-end flex-1 h-full pl-9 pr-8 pt-8 pb-11 bg-white border rounded border-black border-opacity-10">
                <img className="w-14 h-14 rounded-lg" src={disease} alt="SMS" />
                <p className="w-56 h-7 text-lg font-semibold text-gray-900 text-center">
                  Disease Prediction
                </p>
                <p className="opacity-70 w-56 h-1/5 text-base text-center">
                  Dynamic Treatment treatment is also provided
                </p>
              </div>
            </div>
            <div className="w-1/4 h-full">
              <div className="inline-flex flex-col space-y-6 items-center justify-end flex-1 h-full pl-9 pr-8 pt-8 pb-11 bg-white border rounded border-black border-opacity-10">
                <img
                  src={fertile}
                  className="w-14 h-14 rounded-lg"
                  alt="voice assistance"
                />
                <p className="w-60 h-7 text-lg font-semibold text-gray-900 text-center">
                  Fertilizer recommendation
                </p>
                <p className="opacity-70 w-56 h-1/5 text-base text-center">
                  Fertilizer recommendation based on user request
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default CardBar;
