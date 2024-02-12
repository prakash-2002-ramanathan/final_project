import "../../index.css";
import "./body.css";
import FeatureImg from "../img/feature.jpeg";
import CardBar from "../CardBar/CardBar";
import HelpCard from "../HelpCard/HelpCard";

const Body = () => {
  return (
    <div className="body">
      <div className="background-image grid place-items-center my-6">
        <div className="">
          
          <p className="text-6xl font-medium text-center text-green-600 max-w-4xl mb-4">
            Agricultural AI enhancement
          </p>
          <p className="text-l  text-center text-white mb-4">
            by
          </p>
          <p className="text-xl font-bold text-center text-white">
            Prakash Ramanathan
          </p>
          <p className="text-xl font-bold text-center text-white">
            Krteen Anand
          </p>
          <p className="text-xl font-bold text-center text-white">
            Arvind Madavan
          </p>
        </div>
      </div>
      <CardBar />
      
      
    </div>
  );
};

export default Body;
