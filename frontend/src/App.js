
import React, { useState, useEffect } from 'react';
import { LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, RefreshCw, TrendingUp, Eye, CheckCircle, XCircle, Clock,Camera,Zap, Music, X, Check, Shield, Award, Settings, BarChart3, Lock, Image, Video, Mic, AlertTriangle, Database, Activity, Download,BookOpen } from 'lucide-react';
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import WaveSurfer from "wavesurfer.js";
import RegionsPlugin from "wavesurfer.js/dist/plugins/regions.esm.js";


const firebaseConfig = {
  apiKey: "AIzaSyAFRdkrpqX8Vm1fA9XgwAcFAUcfmCdFvHw",
  authDomain: "forgedetect-fdc1e.firebaseapp.com",
  projectId: "forgedetect-fdc1e",
  storageBucket: "forgedetect-fdc1e.firebasestorage.app",
  messagingSenderId: "349091783187",
  appId: "1:349091783187:web:9e758fbc0eaff6e73895e6"
};


const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);

// About Page Component with Animated Deepfake Consequences
const AboutPage = ({ setCurrentView }) => {
  return (
    <div className="min-h-screen bg-gradient-to-r from-black via-[#1a1a1a] to-black">
      {/* Hero Section with Image Grid */}
      <section className="py-20 px-8 bg-gradient-to-br from-teal-900/20 via-purple-900/20 to-orange-900/20">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-5xl font-bold text-white mb-4">
            What is a Deepfake?
          </h1>
          <div className="w-32 h-1 bg-blue-600 mb-8"></div>
          <p className="text-lg text-gray-200 max-w-4xl mb-16 leading-relaxed">
            Deepfakes come in many shapes and forms, and can serve different purposes. Most deepfakes are generated using a combination of the following types of actions.
          </p>

          {/* Image Grid with Categories */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
            
            {/* Mis & Disinformation */}
            <div className="relative group">
              <div className="absolute top-4 left-4 z-10">
                <div className="bg-white px-4 py-2 rounded-full text-black font-bold text-sm">
                  MIS- & DISINFORMATION
                </div>
              </div>
              <div className="rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=800&h=600&fit=crop" 
                  alt="Protest crowd" 
                  className="w-full h-80 object-cover"
                />
                <div className="bg-gray-800 bg-opacity-80 p-6">
                  <p className="text-white text-sm leading-relaxed">
                    Spreading deepfakes in media to manipulate public opinion.
                  </p>
                </div>
              </div>
            </div>

            {/* Fake Profiles */}
            <div className="relative group">
              <div className="absolute top-4 left-4 z-10">
                <div className="bg-white px-4 py-2 rounded-full text-black font-bold text-sm">
                  FAKE PROFILES
                </div>
              </div>
              <div className="rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=800&h=600&fit=crop" 
                  alt="Woman portrait" 
                  className="w-full h-80 object-cover"
                />
                <div className="bg-gray-800 bg-opacity-80 p-6">
                  <p className="text-white text-sm leading-relaxed">
                    Scamming and extorting users with fake profiles on social networks.
                  </p>
                </div>
              </div>
            </div>

            {/* Fake IDs */}
            <div className="relative group">
              <div className="absolute top-4 left-4 z-10">
                <div className="bg-white px-4 py-2 rounded-full text-black font-bold text-sm">
                  FAKE IDS
                </div>
              </div>
              <div className="rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1560250097-0b93528c311a?w=800&h=600&fit=crop" 
                  alt="ID verification" 
                  className="w-full h-80 object-cover"
                />
                <div className="bg-gray-800 bg-opacity-80 p-6">
                  <p className="text-white text-sm leading-relaxed">
                    Forging ID documents to bypass onboarding checks or take over accounts.
                  </p>
                </div>
              </div>
            </div>

            {/* Impersonation */}
            <div className="relative group">
              <div className="absolute top-4 left-4 z-10">
                <div className="bg-white px-4 py-2 rounded-full text-black font-bold text-sm">
                  IMPERSONATION
                </div>
              </div>
              <div className="rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&h=600&fit=crop" 
                  alt="Face scan" 
                  className="w-full h-80 object-cover"
                />
                <div className="bg-gray-800 bg-opacity-80 p-6">
                  <p className="text-white text-sm leading-relaxed">
                    Misleading viewers by representing someone without their consent.
                  </p>
                </div>
              </div>
            </div>

            {/* Nudification */}
            <div className="relative group">
              <div className="absolute top-4 left-4 z-10">
                <div className="bg-white px-4 py-2 rounded-full text-black font-bold text-sm">
                  NUDIFICATION
                </div>
              </div>
              <div className="rounded-2xl overflow-hidden shadow-2xl">
                <div className="w-full h-80 bg-gray-600 backdrop-blur-xl flex items-center justify-center">
                  <p className="text-white text-2xl font-bold">Content Blurred</p>
                </div>
                <div className="bg-gray-800 bg-opacity-80 p-6">
                  <p className="text-white text-sm leading-relaxed">
                    Creating fake nude images of people without their consent.
                  </p>
                </div>
              </div>
            </div>

            {/* Fake News */}
            <div className="relative group">
              <div className="absolute top-4 left-4 z-10">
                <div className="bg-white px-4 py-2 rounded-full text-black font-bold text-sm">
                  FAKE NEWS
                </div>
              </div>
              <div className="rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&h=600&fit=crop" 
                  alt="News broadcast" 
                  className="w-full h-80 object-cover"
                />
                <div className="bg-gray-800 bg-opacity-80 p-6">
                  <p className="text-white text-sm leading-relaxed">
                    Spreading fake news to harm democratic processes.
                  </p>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* Types of Deepfakes Section */}
      <section className="py-20 px-8 bg-gray-900 bg-opacity-30">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-white mb-4">
            Types of Deepfakes
          </h2>
          <div className="w-32 h-1 bg-blue-600 mb-8"></div>
          <p className="text-lg text-gray-200 mb-12 max-w-4xl">
            Most deepfakes are generated using a combination of the following 3 types of actions:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            
            {/* AI-Generation */}
            <div className="bg-gray-800 p-8 rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg transition-shadow">
              <h3 className="text-2xl font-bold text-blue-600 mb-4">AI-GENERATION</h3>
              <p className="text-gray-300 mb-4 leading-relaxed">
                AI-generated images and videos are created by AI models such as Diffusion models (Stable Diffusion, MidJourney, Flux...) or GANs.
              </p>
              <p className="text-gray-300 mb-4 leading-relaxed">
                They are generated out of the blue, or can take a real image as input and modify it.
              </p>
              <p className="text-gray-300 mb-4 leading-relaxed">
                AI-models can also be used to modify parts of an image (inpainting) or extend it (outpainting).
              </p>
            </div>

            {/* Face Swaps */}
            <div className="bg-gray-800 p-8 rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg transition-shadow">
              <h3 className="text-2xl font-bold text-blue-600 mb-4">FACE SWAPS</h3>
              <p className="text-gray-300 mb-4 leading-relaxed">
                Face swaps are a common form of deepfakes. They consist of taking a real image or video of a person, and replacing their face with another person's face.
              </p>
              <p className="text-gray-300 mb-4 leading-relaxed">
                AI models are used to adapt the angle, lighting and expressions of the face to match the provided image or video. Results can be extremely convincing.
              </p>
            </div>

            {/* Face Manipulations */}
            <div className="bg-gray-800 p-8 rounded-2xl border border-gray-200 shadow-sm hover:shadow-lg transition-shadow">
              <h3 className="text-2xl font-bold text-blue-600 mb-4">FACE MANIPULATIONS</h3>
              <p className="text-gray-300 mb-4 leading-relaxed">
                Face manipulations are the result of AI algorithms modifying a person's face, either to change its likeness or to change its emotions and lip movements.
              </p>
              <p className="text-gray-300 mb-4 leading-relaxed">
                This is what so-called lip-sync models use to adapt a person's face to a made-up or modified speech.
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* Detection Section */}
      <section className="py-20 px-8 bg-gray-900 bg-opacity-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            
            <div>
              <h2 className="text-4xl font-bold text-white mb-4">
                Specialized models to detect Face Manipulations.
              </h2>
              <div className="w-32 h-1 bg-blue-600 mb-8"></div>
              <p className="text-gray-300 mb-6 leading-relaxed">
                Our AI models are trained to analyze the outline and consistency of faces in your media.
              </p>
              <p className="text-gray-300 mb-6 leading-relaxed">
                Our models use advanced face analysis to detect <span className="font-semibold">alterations</span>, including <span className="font-semibold">face swaps</span>, face regenerations and AI-generated modifications, ensuring authentic facial representations.
              </p>
              <p className="text-gray-300 mb-6 leading-relaxed">
                The models can be <span className="font-semibold">easily integrated</span> into your existing processes: during user onboarding, <span className="text-teal-600 hover:underline cursor-pointer">content moderation</span>, or media analysis. Processing is done in <span className="font-semibold">near real-time</span>, thereby reducing friction and ensuring a seamless user experience.
              </p>
              <button 
                 onClick={() => setCurrentView("documentation")}
                className="text-teal-600 font-semibold hover:underline text-lg"
              >
                See the documentation
              </button>
            </div>

            <div className="relative">
              <div className="rounded-2xl overflow-hidden shadow-2xl">
                <img 
                  src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop" 
                  alt="Original" 
                  className="w-full h-96 object-cover"
                />
              </div>
              <div className="absolute -bottom-6 -right-6 rounded-2xl overflow-hidden shadow-2xl border-4 border-white">
                <div className="relative">
                  <img 
                    src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop" 
                    alt="Deepfake" 
                    className="w-64 h-48 object-cover"
                  />
                  <div className="absolute bottom-3 right-3 bg-red-500 text-white px-3 py-1 rounded-full flex items-center gap-2 text-sm font-semibold">
                    <div className="w-2 h-2 bg-white rounded-full"></div>
                    Deepfake
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-20 px-8 bg-gray-900">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-white mb-4">
              Advanced Detection Technology
            </h2>
            <div className="w-32 h-1 bg-blue-600 mx-auto mb-8"></div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-8">
              <div className="text-5xl font-bold text-blue-600 mb-3">85%+</div>
              <div className="text-xl font-semibold text-gray-300 mb-2">Accuracy</div>
              <p className="text-gray-400">State-of-the-art detection across all media types</p>
            </div>
            <div className="text-center p-8">
              <div className="text-5xl font-bold text-blue-600 mb-3">Real-Time</div>
              <div className="text-xl font-semibold text-gray-300 mb-2">Analysis</div>
              <p className="text-gray-400">Instant results with detailed confidence scores</p>
            </div>
            <div className="text-center p-8">
              <div className="text-5xl font-bold text-blue-600 mb-3">24/7</div>
              <div className="text-xl font-semibold text-gray-300 mb-2">Continuous Learning</div>
              <p className="text-gray-400">Always adapting to new deepfake techniques</p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
};






const DocumentationPage = () => {
  const [activeTab, setActiveTab] = useState("image");

return (
    <div className="min-h-screen bg-gradient-to-r from-[#121212] via-[#1a1a1a] to-[#121212]">
      {/* Header */}
      <div className="bg-gradient-to-br from-[#1a0a1a] via-[#0a0a1a] to-[#1a0a1a] py-16 px-8 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-64 h-64 bg-pink-500 rounded-full blur-3xl"></div>
          <div className="absolute bottom-10 right-10 w-64 h-64 bg-purple-500 rounded-full blur-3xl"></div>
        </div>
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
              <Shield size={32} className="text-white" />
            </div>
            <h1 className="text-5xl font-bold text-white">
              Detection Documentation
            </h1>
          </div>
          <div className="w-32 h-1 bg-pink-400 mb-6"></div>
          <p className="text-xl text-gray-300 max-w-3xl">
            Comprehensive guide to our deepfake detection APIs for images, videos, and audio
          </p>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="bg-[#2a2a2a] border-b sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-8">
          <div className="flex gap-1">
            <button
              onClick={() => setActiveTab("image")}
              className={`flex items-center gap-2 px-6 py-4 font-semibold transition-all ${
                activeTab === "image"
                  ? "text-pink-500 border-b-2 border-pink-500"
                  : "text-gray-400 hover:text-gray-300"
              }`}
            >
              <Camera size={20} />
              Image Detection
            </button>
            <button
              onClick={() => setActiveTab("video")}
              className={`flex items-center gap-2 px-6 py-4 font-semibold transition-all ${
                activeTab === "video"
                  ? "text-pink-500 border-b-2 border-pink-500"
                  : "text-gray-400 hover:text-gray-300"
              }`}
            >
              <Video size={20} />
              Video Detection
            </button>
            <button
              onClick={() => setActiveTab("audio")}
              className={`flex items-center gap-2 px-6 py-4 font-semibold transition-all ${
                activeTab === "audio"
                  ? "text-pink-500 border-b-2 border-pink-500"
                  : "text-gray-400 hover:text-gray-300"
              }`}
            >
              <Music size={20} />
              Audio Detection
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-8 py-12">
        {/* Image Detection */}
        {activeTab === "image" && (
          <div className="space-y-12">
            {/* Overview */}
            <section>
              <h2 className="text-4xl font-bold text-white mb-6">Overview</h2>
              <div className="bg-[#2a2a2a] rounded-xl p-8 shadow-sm border border-gray-700">
                <p className="text-lg text-gray-300 mb-4 leading-relaxed">
                  The <span className="font-semibold text-pink-500">Image Detection API</span> analyzes images to identify deepfake manipulations, including face swaps, AI-generated content, and facial alterations. Our advanced AI models examine facial features, textures, and inconsistencies to determine authenticity.
                </p>
                <p className="text-lg text-gray-300 leading-relaxed">
                  The API returns detailed confidence scores and can pinpoint specific areas of manipulation within the image.
                </p>
              </div>
            </section>

            {/* How It Works */}
            <section>
              <h3 className="text-3xl font-bold text-white mb-6">How It Works</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-[#2a2a2a] rounded-xl p-6 shadow-sm border border-gray-700">
                  <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mb-4">
                    <Shield className="text-pink-500" size={24} />
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-3">Face Analysis</h4>
                  <p className="text-gray-300">
                    Detects and analyzes all faces in the image, examining facial geometry, texture consistency, and biological patterns.
                  </p>
                </div>
                <div className="bg-[#2a2a2a] rounded-xl p-6 shadow-sm border border-gray-700">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                    <Zap className="text-purple-500" size={24} />
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-3">AI Pattern Detection</h4>
                  <p className="text-gray-300">
                    Identifies artifacts and patterns typical of AI-generated content, face swaps, and digital manipulations.
                  </p>
                </div>
                <div className="bg-[#2a2a2a] rounded-xl p-6 shadow-sm border border-gray-700">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                    <CheckCircle className="text-green-500" size={24} />
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-3">Confidence Scoring</h4>
                  <p className="text-gray-300">
                    Returns detailed confidence scores indicating the likelihood of manipulation and authenticity.
                  </p>
                </div>
              </div>
            </section>
          </div>
        )}

        {/* Video Detection */}
        {activeTab === "video" && (
          <div className="space-y-12">
            <section>
              <h2 className="text-4xl font-bold text-white mb-6">Overview</h2>
              <div className="bg-[#2a2a2a] rounded-xl p-8 shadow-sm border border-gray-700">
                <p className="text-lg text-gray-300 mb-4 leading-relaxed">
                  The <span className="font-semibold text-pink-500">Video Detection API</span> analyzes video content frame-by-frame to detect deepfake manipulations, including face swaps, lip-sync alterations, and AI-generated video content. Our system processes temporal consistency across frames to identify subtle manipulations.
                </p>
                <p className="text-lg text-gray-300 leading-relaxed">
                  The API returns frame-by-frame analysis with timestamps indicating where manipulations occur, along with an overall confidence score for the entire video.
                </p>
              </div>
            </section>

            <section>
              <h3 className="text-3xl font-bold text-white mb-6">How It Works</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-[#2a2a2a] rounded-xl p-6 shadow-sm border border-gray-700">
                  <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mb-4">
                    <Video className="text-pink-500" size={24} />
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-3">Frame Extraction</h4>
                  <p className="text-gray-300">
                    Extracts key frames from the video at optimal intervals for comprehensive analysis without processing redundancy.
                  </p>
                </div>
                <div className="bg-[#2a2a2a] rounded-xl p-6 shadow-sm border border-gray-700">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                    <Shield className="text-purple-500" size={24} />
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-3">Temporal Analysis</h4>
                  <p className="text-gray-300">
                    Analyzes consistency across frames, detecting unnatural movements, flickering, and temporal artifacts typical of deepfakes.
                  </p>
                </div>
                <div className="bg-[#2a2a2a] rounded-xl p-6 shadow-sm border border-gray-700">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                    <CheckCircle className="text-green-500" size={24} />
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-3">Lip-Sync Detection</h4>
                  <p className="text-gray-300">
                    Specifically analyzes mouth movements and audio synchronization to detect lip-sync deepfakes and voice cloning.
                  </p>
                </div>
              </div>
            </section>
          </div>
        )}

        {/* Audio Detection */}
        {activeTab === "audio" && (
          <div className="space-y-12">
            <section>
              <h2 className="text-4xl font-bold text-white mb-6">Overview</h2>
              <div className="bg-[#2a2a2a] rounded-xl p-8 shadow-sm border border-gray-700">
                <p className="text-lg text-gray-300 mb-4 leading-relaxed">
                  The <span className="font-semibold text-pink-500">Audio Detection API</span> analyzes audio recordings to detect voice cloning, synthetic speech, and audio deepfakes. Our advanced models examine acoustic features, speech patterns, and artifacts typical of AI-generated voices.
                </p>
                <p className="text-lg text-gray-300 leading-relaxed">
                  The API returns confidence scores indicating the likelihood that the audio is synthetic or manipulated, along with detailed analysis of suspicious segments.
                </p>
              </div>
            </section>

            <section>
              <h3 className="text-3xl font-bold text-white mb-6">How It Works</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-[#2a2a2a] rounded-xl p-6 shadow-sm border border-gray-700">
                  <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mb-4">
                    <Music className="text-pink-500" size={24} />
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-3">Spectral Analysis</h4>
                  <p className="text-gray-300">
                    Analyzes frequency patterns and spectral characteristics to identify synthetic voice generation artifacts.
                  </p>
                </div>
                <div className="bg-[#2a2a2a] rounded-xl p-6 shadow-sm border border-gray-700">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                    <Shield className="text-purple-500" size={24} />
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-3">Voice Biometrics</h4>
                  <p className="text-gray-300">
                    Examines voice characteristics and biometric markers to detect unnatural patterns in cloned voices.
                  </p>
                </div>
                <div className="bg-[#2a2a2a] rounded-xl p-6 shadow-sm border border-gray-700">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                    <Zap className="text-green-500" size={24} />
                  </div>
                  <h4 className="text-xl font-semibold text-white mb-3">AI Signature Detection</h4>
                  <p className="text-gray-300">
                    Identifies telltale signs of text-to-speech systems, voice conversion tools, and AI voice generators.
                  </p>
                </div>
              </div>
            </section>
          </div>
        )}
      </div>
    </div>
  );
};





// Detection Analytics Admin Dashboard Component
const DetectionAnalyticsAdmin = ({ isAuthenticated, setIsAuthenticated }) => {
  const [activeTab, setActiveTab] = useState("overview");
  const [adminPassword, setAdminPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isFirstTimeSetup, setIsFirstTimeSetup] = useState(false);
  const [passwordError, setPasswordError] = useState("");
  const [detectionHistory, setDetectionHistory] = useState([]);
  const [timeFilter, setTimeFilter] = useState("all");
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    totalDetections: 0,
    fakeDetected: 0,
    realDetected: 0,
    avgConfidence: 0,
    avgProcessingTime: 0,
    reportsDownloaded: 0,
    uniqueUsers: 0,
    imageUploads: 0
  });
// =====================
// Processing Speed UI logic (NO OVERFLOW)
// =====================
const avgTime = stats.avgProcessingTime || 0;

// define a reasonable max for UI scaling
const MAX_TIME = 60;

// value between 0 → 1
const avgTimeScale = Math.min(avgTime / MAX_TIME, 1);


  // Check if admin password exists on component mount
  useEffect(() => {
    const savedPassword = localStorage.getItem('forge_detect_admin_password');
    if (!savedPassword) {
      setIsFirstTimeSetup(true);
    }
  }, []);

  // Fetch detection history from Firebase via backend
  const fetchDetectionHistory = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/analytics/detections?filter=${timeFilter}&limit=100`);
      const data = await response.json();
      
      if (data.success) {
        setDetectionHistory(data.detections);
      }
    } catch (error) {
      console.error("Error fetching detection history:", error);
    }
    setLoading(false);
  };

  // Fetch statistics from Firebase via backend
  const fetchStats = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/analytics/stats');
      const data = await response.json();
      
      if (data.success) {
        setStats(data.stats);
      }
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchDetectionHistory();
      fetchStats();
    }
  }, [isAuthenticated, timeFilter]);

  const handleLogin = (e) => {
    e.preventDefault();
    setPasswordError("");

    if (isFirstTimeSetup) {
      // First time setup - create new password
      if (adminPassword.length < 8) {
        setPasswordError("Password must be at least 8 characters long");
        return;
      }
      if (adminPassword !== confirmPassword) {
        setPasswordError("Passwords do not match");
        return;
      }
      
      // Save the password (in production, hash this!)
      localStorage.setItem('forge_detect_admin_password', adminPassword);
      setIsAuthenticated(true);
      setAdminPassword("");
      setConfirmPassword("");
      setIsFirstTimeSetup(false);
    } else {
      // Regular login - verify password
      const savedPassword = localStorage.getItem('forge_detect_admin_password');
      if (adminPassword === savedPassword) {
        setIsAuthenticated(true);
        setAdminPassword("");
      } else {
        setPasswordError("Incorrect password!");
        setAdminPassword("");
      }
    }
  };

  const handleResetPassword = () => {
    if (window.confirm("Are you sure you want to reset the admin password? You will need to set a new one.")) {
      localStorage.removeItem('forge_detect_admin_password');
      setIsAuthenticated(false);
      setIsFirstTimeSetup(true);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-zinc-900 flex items-center justify-center p-8">
        <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-teal-500 border-opacity-30 rounded-xl p-8 w-full max-w-md">
          <div className="text-center mb-6">
            <Lock className="w-16 h-16 mx-auto mb-4 text-teal-400" />
            <h2 className="text-3xl font-bold text-white mb-2">
              {isFirstTimeSetup ? "First Time Setup" : "Admin Login"}
            </h2>
            <p className="text-gray-400">
              {isFirstTimeSetup 
                ? "Create your admin password to secure the analytics dashboard" 
                : "Enter your password to access analytics"}
            </p>
          </div>
          
          <form onSubmit={handleLogin}>
            {isFirstTimeSetup ? (
              <>
                <div className="mb-4">
                  <label className="block text-gray-300 text-sm mb-2">Create Password</label>
                  <input
                    type="password"
                    value={adminPassword}
                    onChange={(e) => setAdminPassword(e.target.value)}
                    placeholder="Enter new password (min 8 characters)"
                    className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-teal-500 focus:outline-none"
                    required
                  />
                </div>
                <div className="mb-4">
                  <label className="block text-gray-300 text-sm mb-2">Confirm Password</label>
                  <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Confirm your password"
                    className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-teal-500 focus:outline-none"
                    required
                  />
                </div>
              </>
            ) : (
              <div className="mb-4">
                <input
                  type="password"
                  value={adminPassword}
                  onChange={(e) => setAdminPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-teal-500 focus:outline-none"
                  required
                />
              </div>
            )}
            
            {passwordError && (
              <div className="mb-4 p-3 bg-red-900 bg-opacity-50 border border-red-500 border-opacity-50 rounded-lg">
                <p className="text-red-300 text-sm">{passwordError}</p>
              </div>
            )}
            
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 text-white font-bold py-3 rounded-lg transition-all"
            >
              {isFirstTimeSetup ? "Create Password & Access Dashboard" : "Login"}
            </button>
            
            {isFirstTimeSetup && (
              <div className="mt-4 p-3 bg-blue-900 bg-opacity-30 border border-blue-500 border-opacity-30 rounded-lg">
                <p className="text-blue-300 text-sm">
                  ℹ️ <strong>Important:</strong> Remember this password! You'll need it to access the analytics dashboard.
                </p>
              </div>
            )}
            
            {!isFirstTimeSetup && (
              <button
                type="button"
                onClick={() => {
                  if (window.confirm("Forgot your password? This will reset it and you'll need to create a new one.")) {
                    localStorage.removeItem('forge_detect_admin_password');
                    setIsFirstTimeSetup(true);
                    setPasswordError("");
                  }
                }}
                className="w-full mt-3 text-gray-400 hover:text-teal-400 text-sm transition-colors"
              >
                Forgot Password?
              </button>
            )}
          </form>
        </div>
      </div>
    );
  }

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return "N/A";
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    const hours = Math.floor(diff / 3600000);
    if (hours < 1) return `${Math.floor(diff / 60000)} minutes ago`;
    if (hours < 24) return `${hours} hours ago`;
    return date.toLocaleDateString();
  };

  const recentDetections = [...detectionHistory].slice(0, 10);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-zinc-900 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Detection Analytics Dashboard</h1>
            <p className="text-gray-400">Monitor deepfake detection system performance and user activity</p>
          </div>
          <div className="flex gap-4">
            <button
              onClick={() => {
                fetchDetectionHistory();
                fetchStats();
              }}
              className="bg-teal-600 hover:bg-teal-700 text-white font-bold py-3 px-6 rounded-lg transition-all flex items-center gap-2"
              disabled={loading}
            >
              <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
              Refresh
            </button>
            <button
              onClick={handleResetPassword}
              className="bg-yellow-600 hover:bg-yellow-700 text-white font-bold py-3 px-6 rounded-lg transition-all flex items-center gap-2"
            >
              <Lock size={20} />
              Reset Password
            </button>
            <button
              onClick={() => setIsAuthenticated(false)}
              className="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg transition-all"
            >
              Logout
            </button>
          </div>
        </div>

        <div className="flex gap-4 mb-8 border-b border-gray-700">
          {["overview", "detections", "performance"].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 font-semibold transition-all capitalize ${
                activeTab === tab
                  ? "text-teal-400 border-b-2 border-teal-400"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {activeTab === "overview" && (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-teal-500 border-opacity-30 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <Database className="text-teal-400" size={32} />
                  <TrendingUp className="text-green-400" size={20} />
                </div>
                <h3 className="text-gray-400 text-sm mb-2">Total Detections</h3>
                <p className="text-3xl font-bold text-white">{stats.totalDetections}</p>
                <p className="text-green-400 text-sm mt-2">Real-time from Firebase</p>
              </div>

              <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-red-500 border-opacity-30 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <AlertTriangle className="text-red-400" size={32} />
                  <span className="text-red-400 font-bold">
                    {stats.totalDetections > 0 ? Math.round((stats.fakeDetected / stats.totalDetections) * 100) : 0}%
                  </span>
                </div>
                <h3 className="text-gray-400 text-sm mb-2">Fake Detected</h3>
                <p className="text-3xl font-bold text-white">{stats.fakeDetected}</p>
                <p className="text-gray-400 text-sm mt-2">Out of {stats.totalDetections} total</p>
              </div>

              <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-green-500 border-opacity-30 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <CheckCircle className="text-green-400" size={32} />
                  <span className="text-green-400 font-bold">
                    {stats.totalDetections > 0 ? Math.round((stats.realDetected / stats.totalDetections) * 100) : 0}%
                  </span>
                </div>
                <h3 className="text-gray-400 text-sm mb-2">Real Detected</h3>
                <p className="text-3xl font-bold text-white">{stats.realDetected}</p>
                <p className="text-gray-400 text-sm mt-2">Authentic content verified</p>
              </div>

              
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-gray-700 rounded-xl p-6">
                <h3 className="text-xl font-bold text-white mb-4">Detection Distribution</h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-red-400 font-semibold">Fake Content</span>
                      <span className="text-white">
                        {stats.fakeDetected} ({stats.totalDetections > 0 ? Math.round((stats.fakeDetected / stats.totalDetections) * 100) : 0}%)
                      </span>
                    </div>
                    <div className="bg-gray-700 rounded-full h-3">
                      <div
                        className="bg-gradient-to-r from-red-500 to-orange-500 h-3 rounded-full transition-all"
                        style={{ width: `${stats.totalDetections > 0 ? (stats.fakeDetected / stats.totalDetections) * 100 : 0}%` }}
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-green-400 font-semibold">Real Content</span>
                      <span className="text-white">
                        {stats.realDetected} ({stats.totalDetections > 0 ? Math.round((stats.realDetected / stats.totalDetections) * 100) : 0}%)
                      </span>
                    </div>
                    <div className="bg-gray-700 rounded-full h-3">
                      <div
                        className="bg-gradient-to-r from-green-500 to-emerald-500 h-3 rounded-full transition-all"
                        style={{ width: `${stats.totalDetections > 0 ? (stats.realDetected / stats.totalDetections) * 100 : 0}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-gray-700 rounded-xl p-6">
                <h3 className="text-xl font-bold text-white mb-4">System Metrics</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-gray-800 bg-opacity-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <Clock className="text-blue-400" size={24} />
                      <span className="text-gray-300">Avg Processing Time</span>
                    </div>
                    <span className="text-white font-bold">{stats.avgProcessingTime}s</span>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-800 bg-opacity-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <BarChart3 className="text-purple-400" size={24} />
                      <span className="text-gray-300">Avg Confidence</span>
                    </div>
                    <span className="text-white font-bold">{stats.avgConfidence}%</span>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-800 bg-opacity-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <Download className="text-green-400" size={24} />
                      <span className="text-gray-300">Reports Downloaded</span>
                    </div>
                    <span className="text-white font-bold">{stats.reportsDownloaded}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-gray-700 rounded-xl p-6">
              <h2 className="text-2xl font-bold text-white mb-6">Recent Detections (Firebase)</h2>
              {loading ? (
                <div className="text-center py-8">
                  <RefreshCw className="w-12 h-12 mx-auto text-teal-400 animate-spin mb-4" />
                  <p className="text-gray-400">Loading detections from Firebase...</p>
                </div>
              ) : recentDetections.length === 0 ? (
                <div className="text-center py-8">
                  <Database className="w-12 h-12 mx-auto text-gray-600 mb-4" />
                  <p className="text-gray-400">No detections found</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {recentDetections.map(detection => (
                    <div key={detection.id} className="flex items-center justify-between p-4 bg-gray-800 bg-opacity-50 rounded-lg hover:bg-opacity-70 transition-all">
                      <div className="flex items-center gap-4">
                        <div className={`p-2 rounded-lg ${detection.fileType === 'image' ? 'bg-teal-900' : detection.fileType === 'video' ? 'bg-purple-900' : 'bg-orange-900'}`}>
                          {detection.fileType === 'image' && <Image className="text-teal-400" size={24} />}
                          {detection.fileType === 'video' && <Video className="text-purple-400" size={24} />}
                          {detection.fileType === 'audio' && <Mic className="text-orange-400" size={24} />}
                        </div>
                        <div>
                          <h4 className="text-white font-semibold">{detection.fileName}</h4>
                          <p className="text-gray-400 text-sm">{formatTimestamp(detection.timestamp)} • User: {detection.userId}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <p className={`font-bold ${detection.prediction === 'FAKE' ? 'text-red-400' : 'text-green-400'}`}>
                            {detection.prediction}
                          </p>
                          <p className="text-gray-400 text-sm">{detection.confidence}% confidence</p>
                        </div>
                        <div className="text-right">
                          <p className="text-white text-sm">{detection.processingTime}s</p>
                          {detection.downloaded && <Download className="text-green-400 ml-auto" size={16} />}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === "detections" && (
          <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-gray-700 rounded-xl p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-white">All Detections</h2>
              <select
                value={timeFilter}
                onChange={(e) => setTimeFilter(e.target.value)}
                className="bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-700"
              >
                <option value="all">All Time</option>
                <option value="today">Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
              </select>
            </div>
            {loading ? (
              <div className="text-center py-12">
                <RefreshCw className="w-16 h-16 mx-auto text-teal-400 animate-spin mb-4" />
                <p className="text-gray-400">Loading from Firebase...</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-700">
                      <th className="text-left text-gray-400 py-3 px-4">Timestamp</th>
                      <th className="text-left text-gray-400 py-3 px-4">File Name</th>
                      <th className="text-left text-gray-400 py-3 px-4">Type</th>
                      <th className="text-left text-gray-400 py-3 px-4">Result</th>
                      <th className="text-left text-gray-400 py-3 px-4">Confidence</th>
                      <th className="text-left text-gray-400 py-3 px-4">Time</th>
                      <th className="text-left text-gray-400 py-3 px-4">User</th>
                      <th className="text-left text-gray-400 py-3 px-4">Report</th>
                    </tr>
                  </thead>
                  <tbody>
                    {detectionHistory.map(detection => (
                      <tr key={detection.id} className="border-b border-gray-800 hover:bg-gray-800 hover:bg-opacity-30">
                        <td className="py-3 px-4 text-gray-300 text-sm">{formatTimestamp(detection.timestamp)}</td>
                        <td className="py-3 px-4 text-white">{detection.fileName}</td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-1 rounded text-xs ${
                            detection.fileType === 'image' ? 'bg-teal-900 text-teal-300' :
                            detection.fileType === 'video' ? 'bg-purple-900 text-purple-300' :
                            'bg-orange-900 text-orange-300'
                          }`}>
                            {detection.fileType}
                          </span>
                        </td>
                        <td className="py-3 px-4">
                          <span className={`font-bold ${detection.prediction === 'FAKE' ? 'text-red-400' : 'text-green-400'}`}>
                            {detection.prediction}
                          </span>
                        </td>
                        <td className="py-3 px-4 text-white">{detection.confidence}%</td>
                        <td className="py-3 px-4 text-gray-300">{detection.processingTime}s</td>
                        <td className="py-3 px-4 text-gray-300 text-sm">{detection.userId}</td>
                        <td className="py-3 px-4">
                          {detection.downloaded ? (
                            <CheckCircle className="text-green-400" size={18} />
                          ) : (
                            <XCircle className="text-gray-600" size={18} />
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {activeTab === "performance" && (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-gray-700 rounded-xl p-6">
                <h3 className="text-xl font-bold text-white mb-4">Processing Speed</h3>
                <div className="space-y-4">
                  <div className="mb-6">
  {/* Label */}
  <p className="text-sm text-gray-400 mb-1">Average Time</p>

  {/* Value */}
  <p className="text-2xl font-bold text-white mb-2">
    {stats.avgProcessingTime.toFixed(2)}s
  </p>

  {/* Progress Bar */}
  <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
    <div
      className="h-3 bg-blue-500 rounded-full origin-left transition-transform duration-500"
      style={{ transform: `scaleX(${avgTimeScale})` }}
    />
  </div>
</div>

                  <div className="flex justify-between p-3 bg-gray-800 bg-opacity-50 rounded">
                    <span className="text-gray-300">Fastest Detection</span>
                    <span className="text-green-400 font-bold">
                      {detectionHistory.length > 0 ? Math.min(...detectionHistory.map(d => d.processingTime || 0)) : 0}s
                    </span>
                  </div>
                  <div className="flex justify-between p-3 bg-gray-800 bg-opacity-50 rounded">
                    <span className="text-gray-300">Slowest Detection</span>
                    <span className="text-orange-400 font-bold">
                      {detectionHistory.length > 0 ? Math.max(...detectionHistory.map(d => d.processingTime || 0)) : 0}s
                    </span>
                  </div>
                </div>
              </div>

              <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-gray-700 rounded-xl p-6">
                <h3 className="text-xl font-bold text-white mb-4">Confidence Distribution</h3>
                <div className="space-y-4">
                  {[
                    { range: '90-100%', color: 'green', count: detectionHistory.filter(d => d.confidence >= 90).length },
                    { range: '80-89%', color: 'blue', count: detectionHistory.filter(d => d.confidence >= 80 && d.confidence < 90).length },
                    { range: '70-79%', color: 'yellow', count: detectionHistory.filter(d => d.confidence >= 70 && d.confidence < 80).length },
                    { range: 'Below 70%', color: 'red', count: detectionHistory.filter(d => d.confidence < 70).length }
                  ].map(item => (
                    <div key={item.range}>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-gray-300">{item.range}</span>
                        <span className="text-white font-bold">
                          {item.count} ({stats.totalDetections > 0 ? Math.round((item.count / stats.totalDetections) * 100) : 0}%)
                        </span>
                      </div>
                      <div className="bg-gray-700 rounded-full h-3">
                        <div
                          className={`bg-gradient-to-r ${
                            item.color === 'green' ? 'from-green-500 to-emerald-500' :
                            item.color === 'blue' ? 'from-blue-500 to-cyan-500' :
                            item.color === 'yellow' ? 'from-yellow-500 to-orange-500' :
                            'from-red-500 to-pink-500'
                          } h-3 rounded-full`}
                          style={{ width: `${stats.totalDetections > 0 ? (item.count / stats.totalDetections) * 100 : 0}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="bg-black bg-opacity-40 backdrop-blur-sm border border-gray-700 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-4">System Health</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-green-900 bg-opacity-30 border border-green-500 border-opacity-30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-green-400 font-semibold">API Status</span>
                    <CheckCircle className="text-green-400" size={20} />
                  </div>
                  <p className="text-white text-2xl font-bold">Online</p>
                  <p className="text-green-400 text-sm">Firebase Connected</p>
                </div>
                <div className="p-4 bg-blue-900 bg-opacity-30 border border-blue-500 border-opacity-30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-blue-400 font-semibold">Model Version</span>
                    <Settings className="text-blue-400" size={20} />
                  </div>
                  <p className="text-white text-2xl font-bold">v2.1.4</p>
                  <p className="text-blue-400 text-sm">Latest stable</p>
                </div>
                <div className="p-4 bg-purple-900 bg-opacity-30 border border-purple-500 border-opacity-30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-purple-400 font-semibold">Server Load</span>
                    <Activity className="text-purple-400" size={20} />
                  </div>
                  <p className="text-white text-2xl font-bold">42%</p>
                  <p className="text-purple-400 text-sm">Optimal range</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};


// Home Page Component
const HomePage = ({ handlePageChange }) => {
  
  return (
    <>
      {/* Hero Landing Section */}
      <section className="relative flex flex-col items-center justify-center text-center py-32 px-8 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-teal-900/20 via-purple-900/20 to-orange-900/20 animate-pulse"></div>
        <div className="relative z-10">
          <h2 className="text-7xl font-bold mb-6 bg-gradient-to-r from-teal-400 via-purple-400 to-orange-400 bg-clip-text text-transparent">
            MULTI-MODAL DEEPFAKE DETECTION
          </h2>
          <p className="text-2xl text-gray-300 max-w-4xl mb-12 leading-relaxed">
            Powered by cutting-edge AI to protect you from digital deception
          </p>
          <div className="flex gap-6 justify-center flex-wrap">
            <div className="flex items-center gap-2 bg-teal-900 bg-opacity-30 px-6 py-3 rounded-full border border-teal-400 border-opacity-30">
              <Shield className="text-teal-400" size={24} />
              <span className="text-teal-400 font-semibold">AI-Based Detection</span>
            </div>
            <div className="flex items-center gap-2 bg-purple-900 bg-opacity-30 px-6 py-3 rounded-full border border-purple-400 border-opacity-30">
              <Activity className="text-purple-400" size={24} />
              <span className="text-purple-400 font-semibold">Real-Time Analysis</span>
            </div>
            <div className="flex items-center gap-2 bg-orange-900 bg-opacity-30 px-6 py-3 rounded-full border border-orange-400 border-opacity-30">
              <Database className="text-orange-400" size={24} />
              <span className="text-orange-400 font-semibold">Secure Cloud Backend</span>
            </div>
          </div>
        </div>
      </section>

      {/* Detection Modules */}
      <section className="py-20 px-8">
        <div className="max-w-7xl mx-auto">
          <h3 className="text-4xl font-bold text-center text-white mb-16">
            Choose Your Detection Module
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Image Detection */}
            <div 
              onClick={() => handlePageChange("image")}
              className="group relative bg-gradient-to-br from-teal-900 via-cyan-900 to-blue-900 bg-opacity-40 backdrop-blur-sm border border-teal-500 border-opacity-30 rounded-2xl p-8 hover:scale-105 transition-all duration-500 hover:shadow-2xl hover:shadow-teal-500/50 cursor-pointer"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-teal-400/0 to-cyan-400/0 group-hover:from-teal-400/10 group-hover:to-cyan-400/10 transition-all duration-500 rounded-2xl"></div>
              <div className="relative z-10">
                <div className="w-20 h-20 mx-auto mb-6 text-teal-400 group-hover:scale-110 transition-transform duration-500">
                  <Image size={80} />
                </div>
                <h4 className="text-3xl font-bold text-teal-400 mb-4">IMAGE DETECTION</h4>
                <p className="text-gray-300 mb-6 leading-relaxed">
                  Advanced neural networks analyze facial features, lighting inconsistencies, and digital artifacts.
                </p>
                <div className="space-y-3 mb-8">
                  <div className="flex items-center gap-3 text-teal-300">
                    <CheckCircle size={20} />
                    <span>Face Swap Detection</span>
                  </div>
                  <div className="flex items-center gap-3 text-teal-300">
                    <CheckCircle size={20} />
                    <span>Synthetic Portrait Analysis</span>
                  </div>
                  <div className="flex items-center gap-3 text-teal-300">
                    <CheckCircle size={20} />
                    <span>GradCAM Visualization</span>
                  </div>
                </div>
                <button className="w-full bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 text-white font-bold py-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2">
                  <span>Start Image Analysis</span>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Video Detection */}
              <div
                onClick={() => handlePageChange("video")}
                className="group relative bg-gradient-to-br from-purple-900 via-indigo-900 to-violet-900 bg-opacity-40 backdrop-blur-sm border border-purple-500 border-opacity-30 rounded-2xl p-8 hover:scale-105 transition-all duration-500 hover:shadow-2xl hover:shadow-purple-500/50 cursor-pointer"
              >
              <div className="relative z-10">
                <div className="w-20 h-20 mx-auto mb-6 text-purple-400 group-hover:scale-110 transition-transform duration-500">
                  <Video size={80} />
                </div>
                <h4 className="text-3xl font-bold text-purple-400 mb-4">VIDEO DETECTION</h4>
                <p className="text-gray-300 mb-6 leading-relaxed">
                  Temporal analysis identifies lip-sync errors and facial inconsistencies in videos.
                </p>
                <div className="space-y-3 mb-8">
                  <div className="flex items-center gap-3 text-purple-300">
                    <CheckCircle size={20} />
                    <span>Frame-by-Frame Analysis</span>
                  </div>
                  <div className="flex items-center gap-3 text-purple-300">
                    <CheckCircle size={20} />
                    <span>Lip-Sync Detection</span>
                  </div>
                  <div className="flex items-center gap-3 text-purple-300">
                    <CheckCircle size={20} />
                    <span>Motion Artifact Tracking</span>
                  </div>
                </div>
                <button
                  className="w-full bg-gradient-to-r from-purple-500 to-violet-500 hover:from-purple-600 hover:to-violet-600 text-white font-bold py-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2"
                >
                  <span>Start Video Analysis</span>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </button>

              </div>
            </div>

            {/* Audio Detection */}
            <div className="group relative bg-gradient-to-br from-orange-900 via-red-900 to-pink-900 bg-opacity-40 backdrop-blur-sm border border-orange-500 border-opacity-30 rounded-2xl p-8 hover:scale-105 transition-all duration-500 hover:shadow-2xl hover:shadow-orange-500/50">
              <div className="relative z-10">
                <div className="w-20 h-20 mx-auto mb-6 text-orange-400 group-hover:scale-110 transition-transform duration-500">
                  <Mic size={80} />
                </div>
                <h4 className="text-3xl font-bold text-orange-400 mb-4">AUDIO DETECTION</h4>
                <p className="text-gray-300 mb-6 leading-relaxed">
                  Spectral analysis detects AI-generated speech and voice cloning.
                </p>
                <div className="space-y-3 mb-8">
                  <div className="flex items-center gap-3 text-orange-300">
                    <CheckCircle size={20} />
                    <span>Voice Cloning Detection</span>
                  </div>
                  <div className="flex items-center gap-3 text-orange-300">
                    <CheckCircle size={20} />
                    <span>Spectral Analysis</span>
                  </div>
                  <div className="flex items-center gap-3 text-orange-300">
                    <CheckCircle size={20} />
                    <span>TTS Identification</span>
                  </div>
                </div>
                <button
                  onClick={() => handlePageChange("audio")}
                  className="w-full bg-gradient-to-r from-orange-500 to-pink-500 hover:from-orange-600 hover:to-pink-600 text-white font-bold py-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2"
                >
                  <span>Start Audio Analysis</span>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </button>

              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-8 bg-black bg-opacity-30">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-4xl font-bold text-center text-white mb-16">
            How It Works
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { num: 1, title: "Upload", desc: "Submit your media file", color: "teal" },
              { num: 2, title: "Analyze", desc: "AI processes features", color: "purple" },
              { num: 3, title: "Detect", desc: "Identify anomalies", color: "orange" },
              { num: 4, title: "Report", desc: "Get detailed results", color: "green" }
            ].map((step) => (
              <div key={step.num} className="text-center">
                <div className={`w-16 h-16 mx-auto mb-4 bg-${step.color}-900 bg-opacity-50 rounded-full flex items-center justify-center`}>
                  <span className={`text-3xl font-bold text-${step.color}-400`}>{step.num}</span>
                </div>
                <h4 className={`text-xl font-bold text-${step.color}-400 mb-2`}>{step.title}</h4>
                <p className="text-gray-300">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 text-center">
        <div className="max-w-4xl mx-auto px-8">
          <h3 className="text-4xl font-bold text-white mb-6">
            Ready to Verify Your Media?
          </h3>
          <p className="text-xl text-gray-300 mb-8">
            Start detecting deepfakes with our AI-powered platform
          </p>
          <button
            onClick={() => handlePageChange("image")}
            className="bg-gradient-to-r from-teal-500 via-purple-500 to-orange-500 hover:from-teal-600 hover:via-purple-600 hover:to-orange-600 text-white font-bold py-4 px-12 rounded-lg text-xl transition-all duration-300 transform hover:scale-105"
          >
            Get Started Now →
          </button>
        </div>
      </section>
    </>
  );
};

// Detection Page Component
const DetectionPage = ({ currentPage, file, setFile, result,videoResult,audioResult, loading, error, handleSubmit }) => {
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  return (
    <>
      <section className="flex flex-col items-center justify-center text-center py-20">
        <h2 className={`text-5xl font-bold mb-6 ${
          currentPage === "image" ? "text-teal-400" : 
          currentPage === "video" ? "text-purple-400" : "text-orange-400"
        }`}>
          {currentPage === "image" ? "Image DeepFake Detection" :
           currentPage === "video" ? "Video DeepFake Detection" : "Audio DeepFake Detection"}
        </h2>
        <p className="text-lg text-gray-300 max-w-3xl mb-8 leading-relaxed">
          Upload your {currentPage} for instant AI-powered deepfake analysis
        </p>
      </section>

      <section className="flex flex-col items-center py-16">
        <div className={`bg-gradient-to-br ${
          currentPage === "image" ? "from-teal-900 via-blue-900 to-cyan-900 border-teal-500" :
          currentPage === "video" ? "from-purple-900 via-indigo-900 to-violet-900 border-purple-500" :
          "from-orange-900 via-red-900 to-pink-900 border-orange-500"
        } bg-opacity-40 backdrop-blur-sm border border-opacity-30 p-12 rounded-xl shadow-2xl w-96 text-center`}>
          <div className={`border-2 border-dashed ${
            currentPage === "image" ? "border-teal-400" :
            currentPage === "video" ? "border-purple-400" : "border-orange-400"
          } border-opacity-50 rounded-lg p-8 mb-6`}>
            <input
              type="file"
              accept={currentPage === "image" ? "image/*" : currentPage === "video" ? "video/*" : "audio/*"}
              onChange={handleFileChange}
            />
            <label htmlFor={`${currentPage}-upload`} className="cursor-pointer flex flex-col items-center">
              {currentPage === "image" && <Image className="text-teal-400 mb-4" size={64} />}
              {currentPage === "video" && <Video className="text-purple-400 mb-4" size={64} />}
              {currentPage === "audio" && <Mic className="text-orange-400 mb-4" size={64} />}
              <span className={`${
                currentPage === "image" ? "text-teal-400" :
                currentPage === "video" ? "text-purple-400" : "text-orange-400"
              } font-semibold text-lg`}>
                {file ? file.name : currentPage === "image" ? "Choose Image" : `${currentPage} (Coming Soon)`}
              </span>
            </label>
          </div>
          
          {error && (
            <div className="mb-4 p-3 bg-red-900 bg-opacity-50 rounded-lg">
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          )}
          
          <button
  onClick={handleSubmit}
  disabled={!file || loading}
  className={`w-full px-6 py-3 ${
    currentPage === "image" ? "bg-teal-500 hover:bg-teal-600" :
    currentPage === "video" ? "bg-purple-500 hover:bg-purple-600" :
    "bg-orange-500 hover:bg-orange-600"
  } rounded-lg font-semibold transition-all ${
    (!file || loading) ? "opacity-50 cursor-not-allowed" : ""
  }`}
>
  {loading
    ? "ANALYZING..."
    : currentPage === "image"
    ? "ANALYZE IMAGE"
    : currentPage === "video"
    ? "ANALYZE VIDEO"
    : "ANALYZE AUDIO"}
</button>

        </div>

        {result && currentPage === "image" && (
          <div className="mt-8 p-6 bg-teal-800 bg-opacity-30 border border-teal-500 border-opacity-30 rounded-lg w-full max-w-4xl">
            <h3 className="font-semibold mb-4 text-teal-400 text-2xl">Analysis Results</h3>
            <div className="grid grid-cols-3 gap-6">
              <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                <h4 className="text-teal-300 font-semibold mb-2">Prediction</h4>
                <p className={`text-2xl font-bold ${result.prediction === 'REAL' ? 'text-green-400' : 'text-red-400'}`}>
                  {result.prediction}
                </p>
              </div>
              <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                <h4 className="text-teal-300 font-semibold mb-2">Confidence</h4>
                <p className="text-2xl font-bold text-white">{result.confidence}%</p>
              </div>
              <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                <h4 className="text-teal-300 font-semibold mb-2">Status</h4>
                <p className="text-green-400 font-bold">Complete</p>
              </div>
            </div>
          </div>
        )}

        {videoResult && currentPage === "video" && (
          <div className="mt-8 p-6 bg-purple-800 bg-opacity-30 border border-purple-500 border-opacity-30 rounded-lg w-full max-w-4xl text-center">
            
            <h3 className="text-2xl font-bold text-purple-400 mb-4">
              🎬 Video Analysis Results
            </h3>

            <div className="grid grid-cols-3 gap-6 mb-6">
              <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                <h4 className="text-purple-300 font-semibold mb-2">Prediction</h4>
                <p className={`text-2xl font-bold ${
  videoResult?.prediction === "REAL" ? "text-green-400" : "text-red-400"
}`}>
  {videoResult?.prediction ?? "--"}
</p>

              </div>

              <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                <h4 className="text-purple-300 font-semibold mb-2">Confidence</h4>
                <p className="text-2xl font-bold text-white">
  {videoResult?.confidence ?? "--"}%
</p>

              </div>

              <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                <h4 className="text-purple-300 font-semibold mb-2">Status</h4>
                <p className="text-green-400 font-bold">Complete</p>
              </div>
            </div>

            <div className="mt-6">
              <h4 className="text-purple-300 font-semibold mb-3">
                🎥 Annotated Output Video
              </h4>

              <video
  controls
  className="w-full rounded-lg border border-purple-500"
  src={videoResult.video_url}
/>


              {videoResult?.download_url && (
  <button
    onClick={() => window.open(videoResult.download_url, "_blank")}
    className="mt-4 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2"
  >
    ⬇️ Download Output Video
  </button>
)}

            </div>
          </div>
        )}


{audioResult && currentPage === "audio" && (
  <div className="mt-8 p-6 bg-orange-900 bg-opacity-30 border border-orange-500 rounded-lg max-w-3xl mx-auto text-center">
    <h3 className="text-2xl font-bold text-orange-400 mb-4">
      🎧 Audio Deepfake Analysis
    </h3>

    <p className={`text-3xl font-bold ${
      audioResult.prediction === "REAL" ? "text-green-400" : "text-red-400"
    }`}>
      {audioResult.prediction}
    </p>

    <p className="text-xl text-white mt-2">
      Confidence: {audioResult.confidence}%
    </p>

    <p className="text-lg text-gray-300 mt-2">
      Risk Level: <strong>{audioResult.risk}</strong>
    </p>

    <audio controls className="mt-4 w-full">
      <source src={URL.createObjectURL(file)} />
    </audio>
  </div>
)}



      </section>
    </>
  );
};

function App() {
  const [currentPage, setCurrentPage] = useState("image");
  const [currentView, setCurrentView] = useState("home");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [videoResult, setVideoResult] = useState(null);
  const [audioResult, setAudioResult] = useState(null);
  const waveformRef = React.useRef(null);
  const waveSurferRef = React.useRef(null);
  const [downloadingReport, setDownloadingReport] = useState(false);
  const [originalImageData, setOriginalImageData] = useState(null);
  const [isAdminAuthenticated, setIsAdminAuthenticated] = useState(false);
  const [estimatedTime, setEstimatedTime] = useState(null);



  useEffect(() => {
  if (!file || !audioResult) return;

  // Destroy old instance
  if (waveSurferRef.current) {
    waveSurferRef.current.destroy();
  }

  waveSurferRef.current = WaveSurfer.create({
  container: waveformRef.current,
  waveColor: "#fb923c",
  progressColor: "#f97316",
  height: 90,
  barWidth: 2,
  responsive: true,
  plugins: [
    RegionsPlugin.create()
  ]
});


  waveSurferRef.current.load(URL.createObjectURL(file));


  return () => waveSurferRef.current?.destroy();
}, [file, audioResult]);
  

const handleSubmit = async () => {
  if (!file) {
    setError("Please select a file first");
    return;
  }

  setLoading(true);
  setError(null);
  setResult(null);
  setVideoResult(null);
  setAudioResult(null);
  
  const formData = new FormData();
  formData.append("file", file);

  let endpoint = "";

  if (currentPage === "image") {
    endpoint = "http://127.0.0.1:5000/predict";
  } else if (currentPage === "video") {
    endpoint = "http://127.0.0.1:5000/predict-video";
  } else if (currentPage === "audio") {
    endpoint = "http://127.0.0.1:5000/predict-audio";
  } else {
    setError("Invalid detection type");
    setLoading(false);
    return;
  }

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Detection failed");
    }

        if (currentPage === "image") {
      setResult(data);
    } else if (currentPage === "video") {
      setVideoResult(data);
    } else if (currentPage === "audio") {
      setAudioResult(data);
    }

  } catch (err) {
    console.error(err);
    setError(err.message || "Server error");
  } finally {
    setLoading(false);
  }
};





  const handleDownloadReport = async () => {
    if (!result || !result.analysis_data) {
      setError("No analysis data available for report generation.");
      return;
    }

    setDownloadingReport(true);
    setError("");

    try {
      const payload = {
        analysis_data: result.analysis_data,
        original_image_data: originalImageData,
        session_id: result.session_id
      };

      const response = await fetch("http://127.0.0.1:5000/download-report", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      
      const timestamp = new Date().toISOString().slice(0, 19).replace(/[-:]/g, '').replace('T', '_');
      link.download = `forge_detect_report_${timestamp}.pdf`;
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

    } catch (err) {
      console.error("Error downloading report:", err);
      setError("⚠️ Error generating report. Please try again.");
    }

    setDownloadingReport(false);
  };

  const handleFileChange = (e) => {
  const selectedFile = e.target.files[0];
  if (!selectedFile) return;

  setError("");
  setResult(null);
  setVideoResult(null);
  setAudioResult(null);


  // Size limit (example: 200MB for video, 10MB for image)
  const maxSize =
    currentPage === "image" ? 10 * 1024 * 1024 :
    currentPage === "video" ? 200 * 1024 * 1024 :
    50 * 1024 * 1024;

  if (selectedFile.size > maxSize) {
    setError(
      currentPage === "image"
        ? "Image size must be under 10MB."
        : currentPage === "video"
        ? "Video size must be under 200MB."
        : "Audio file too large."
    );
    setFile(null);
    return;
  }

  // Allowed MIME types
  const allowedTypes = {
    image: [
      "image/jpeg",
      "image/jpg",
      "image/png",
      "image/gif",
      "image/webp"
    ],
    video: [
      "video/mp4",
      "video/avi",
      "video/mov",
      "video/webm",
      "video/mkv"
    ],
    audio: [
      "audio/mpeg",
      "audio/wav",
      "audio/flac",
      "audio/mp4",
      "audio/x-m4a"
    ]
  };

  if (!allowedTypes[currentPage]?.includes(selectedFile.type)) {
    setError(
      currentPage === "image"
        ? "Invalid image file type."
        : currentPage === "video"
        ? "Invalid video file type."
        : "Invalid audio file type."
    );
    setFile(null);
    return;
  }

  setFile(selectedFile);

  // Only read image data for image detection
  if (currentPage === "image") {
    const reader = new FileReader();
    reader.onload = (e) => {
      const base64Data = e.target.result.split(",")[1];
      setOriginalImageData(base64Data);
    };
    reader.onerror = () => {
      setError("Error processing image file.");
    };
    reader.readAsDataURL(selectedFile);
  }
  if (currentPage === "video") {
  const video = document.createElement("video");
  video.preload = "metadata";

  video.onloadedmetadata = () => {
    window.URL.revokeObjectURL(video.src);

    const durationSec = video.duration;

    // Rough estimate: ~1 min processing per 30 sec video
    const estimatedMinutes = Math.ceil(durationSec / 30);

    setEstimatedTime(estimatedMinutes);
  };

  video.src = URL.createObjectURL(selectedFile);
}

};


  const handlePageChange = (page) => {
    setCurrentPage(page);
    setCurrentView("detection");
    setFile(null);
    setResult(null);
    setLoading(false);
    setError("");
    setDownloadingReport(false);
  };

  return (
    <div className="min-h-screen text-white bg-gradient-to-r from-black via-[#1a1a1a] to-black">
      {/* Navbar */}
      <nav className="flex justify-between items-center px-10 py-4 bg-black bg-opacity-50 backdrop-blur-sm sticky top-0 z-50">
        <h1 
          className="text-2xl font-bold text-teal-400 cursor-pointer"
          onClick={() => setCurrentView("home")}
        >
          FORGE DETECT
        </h1>
        <div className="flex gap-6">
          <button 
            onClick={() => setCurrentView("home")} 
            className={`hover:text-cyan-400 transition-colors px-3 py-1 rounded ${currentView === "home" ? "bg-cyan-500 bg-opacity-20 text-cyan-400" : "text-white"}`}
          >
            Home
          </button>
          <button 
            onClick={() => setCurrentView("about")} 
            className={`hover:text-indigo-400 transition-colors px-3 py-1 rounded ${currentView === "about" ? "bg-indigo-500 bg-opacity-20 text-indigo-400" : "text-white"}`}
          >
            About
          </button>
         
          <button 
            onClick={() => handlePageChange("image")} 
            className={`hover:text-teal-400 transition-colors px-3 py-1 rounded ${currentView === "detection" && currentPage === "image" ? "bg-teal-500 bg-opacity-20 text-teal-400" : "text-white"}`}
          >
            Image Detection
          </button>
          <button 
            onClick={() => handlePageChange("video")} 
            className={`hover:text-purple-400 transition-colors px-3 py-1 rounded ${currentView === "detection" && currentPage === "video" ? "bg-purple-500 bg-opacity-20 text-purple-400" : "text-white"}`}
          >
            Video Detection
          </button>
          <button 
            onClick={() => handlePageChange("audio")} 
            className={`hover:text-orange-400 transition-colors px-3 py-1 rounded ${currentView === "detection" && currentPage === "audio" ? "bg-orange-500 bg-opacity-20 text-orange-400" : "text-white"}`}
          >
            Audio Detection
          </button>
           <button 
            onClick={() => setCurrentView("documentation")} 
            className={`hover:text-violet-400 transition-colors px-3 py-1 rounded ${currentView === "documentation" ? "bg-violet-500 bg-opacity-20 text-violet-400" : "text-white"}`}
          >
            Documentation
          </button>
          <button 
            onClick={() => setCurrentView("admin")}
            className={`hover:text-emerald-400 transition-colors px-3 py-1 rounded ${currentView === "admin" ? "bg-emerald-500 bg-opacity-20 text-emerald-400" : "text-white"}`}
          >
            Analytics
          </button>
        </div>
      </nav>

      {/* Conditional Page Rendering */}
      {currentView === "home" ? (
  <HomePage handlePageChange={handlePageChange} />
) : currentView === "about" ? (
  <AboutPage setCurrentView={setCurrentView} />
) : currentView === "documentation" ? (
  <DocumentationPage />

) : currentView === "admin" ? (
  <DetectionAnalyticsAdmin 
    isAuthenticated={isAdminAuthenticated}
    setIsAuthenticated={setIsAdminAuthenticated}
  />
) : (
        <>
          {/* Hero Section */}
          <section className="flex flex-col items-center justify-center text-center py-20">
            <h2 className={`text-5xl font-bold mb-6 ${
              currentPage === "image" ? "text-teal-400" : 
              currentPage === "video" ? "text-purple-400" : "text-orange-400"
            }`}>
              {currentPage === "image" ? "Image DeepFake Detection" :
               currentPage === "video" ? "Video DeepFake Analysis" : "Audio Synthesis Detection"}
            </h2>
            <p className="text-lg text-gray-300 max-w-3xl mb-8 leading-relaxed">
              {currentPage === "image" ? 
                "Advanced AI-powered detection for manipulated images, face swaps, and synthetic portraits. Upload your image and get instant analysis with confidence scores and visual explanations." :
               currentPage === "video" ?
                "Comprehensive temporal analysis for detecting deepfake videos, lip-sync manipulation, and face replacements." :
                "Sophisticated spectral analysis for identifying AI-generated speech, voice cloning, and synthetic audio."
              }
            </p>
          </section>

          {/* Upload Section */}
          <section id="detect" className="flex flex-col items-center py-16">
            
            {/* Image Detection Module */}
            {currentPage === "image" && (
              <>
                <div className="mb-8 text-center">
                  <h3 className="text-3xl font-bold text-teal-400 mb-4">🖼️ Image Analysis Module</h3>
                  <p className="text-gray-300">Upload your image for AI-powered deepfake detection</p>
                  <p className="text-teal-400 text-sm mt-2">✅ Connected to Firebase Database</p>
                </div>
                
                <div className="bg-gradient-to-br from-teal-900 via-blue-900 to-cyan-900 bg-opacity-40 backdrop-blur-sm border border-teal-500 border-opacity-30 p-12 rounded-xl shadow-2xl w-96 text-center">
                  <div className="border-2 border-dashed border-teal-400 border-opacity-50 rounded-lg p-8 mb-6 hover:border-opacity-100 transition-all duration-300">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileChange}
                      className="hidden"
                      id="image-upload"
                    />
                    <label 
                      htmlFor="image-upload" 
                      className="cursor-pointer flex flex-col items-center justify-center"
                    >
                      <div className="w-16 h-16 mb-4 text-teal-400">
                        <svg fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="text-teal-400 font-semibold text-lg">
                        {file ? file.name : "📷 Choose Image"}
                      </span>
                      <span className="text-gray-400 text-sm mt-2">
                        Click to upload an image for detection
                      </span>
                    </label>
                  </div>
                  
                  {error && (
                    <div className="mb-4 p-3 bg-red-900 bg-opacity-50 border border-red-500 border-opacity-50 rounded-lg">
                      <p className="text-red-300 text-sm">{error}</p>
                    </div>
                  )}
                  
                  <button
                    onClick={handleSubmit}
                    disabled={!file || loading}
                    className="w-full px-6 py-3 bg-teal-500 hover:bg-teal-600 rounded-lg font-semibold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? "🔄 ANALYZING IMAGE..." : "🚀 ANALYZE IMAGE"}
                  </button>
                  
                  <p className="text-gray-400 text-sm mt-4">
                    📋 Supported: JPG, PNG, GIF, WEBP (Max: 10MB)
                  </p>
                </div>
              </>
            )}

            {/* Results Display */}
            {result && (
              <div className="mt-8 p-6 backdrop-blur-sm border rounded-lg text-lg w-full max-w-4xl text-center shadow-xl bg-teal-800 bg-opacity-30 border-teal-500 border-opacity-30">
                <h3 className="font-semibold mb-4 text-teal-400 text-2xl">🔍 Analysis Results</h3>
                
                {result.firebase_id && (
                  <div className="mb-4 p-3 bg-green-900 bg-opacity-30 border border-green-500 border-opacity-30 rounded-lg">
                    <p className="text-green-300 text-sm">
                      ✅ Results saved to Firebase (ID: {result.firebase_id})
                    </p>
                  </div>
                )}
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                  <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                    <h4 className="text-teal-300 font-semibold mb-2">Prediction</h4>
                    <p className={`text-2xl font-bold ${result.prediction === 'REAL' ? 'text-green-400' : 'text-red-400'}`}>
                      {result.prediction}
                    </p>
                  </div>
                  
                  <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                    <h4 className="text-teal-300 font-semibold mb-2">Confidence</h4>
                    <p className="text-2xl font-bold text-white">
                      {result.confidence}%
                    </p>
                  </div>

                  <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                    <h4 className="text-teal-300 font-semibold mb-2">Risk Level</h4>
                    <p className={`text-lg font-bold ${
                      result.prediction === 'FAKE' && result.confidence > 80 ? 'text-red-400' :
                      result.prediction === 'FAKE' && result.confidence > 60 ? 'text-yellow-400' : 'text-green-400'
                    }`}>
                      {result.prediction === 'FAKE' && result.confidence > 80 ? '⚠️ HIGH' :
                       result.prediction === 'FAKE' && result.confidence > 60 ? '⚡ MEDIUM' : '✅ LOW'}
                    </p>
                  </div>
                </div>

                {result.message && (
                  <p className="text-gray-300 mb-6">{result.message}</p>
                )}

                <div className="mb-6">
                  <button
                    onClick={handleDownloadReport}
                    disabled={downloadingReport}
                    className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold py-4 px-10 rounded-lg shadow-lg transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center gap-3 mx-auto text-lg"
                  >
                    <div className="w-6 h-6">
                      <svg fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v3.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V8z" clipRule="evenodd"/>
                      </svg>
                    </div>
                    {downloadingReport ? "📄 Generating Professional Report..." : "📄 Download Professional Report"}
                  </button>
                  <p className="text-gray-400 text-sm mt-3">
                    Generate a comprehensive PDF report with visual analysis, technical details, and recommendations
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                    <h4 className="text-teal-300 font-semibold mb-4">📷 Original Image</h4>
                    {file && (
                      <img 
                        src={URL.createObjectURL(file)} 
                        alt="Original uploaded"
                        className="rounded-lg border border-teal-500 border-opacity-30 max-w-full h-48 object-contain mx-auto shadow-lg"
                      />
                    )}
                  </div>

                  {result.heatmap && (
                    <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                      <h4 className="text-teal-300 font-semibold mb-4">🎯 AI Focus Areas</h4>
                      <p className="text-gray-400 text-sm mb-4">
                        Red regions show where the AI focused during analysis
                      </p>
                      <img 
                        src={`data:image/png;base64,${result.heatmap}`} 
                        alt="GradCAM Heatmap"
                        className="rounded-lg border border-teal-500 border-opacity-30 max-w-full h-48 object-contain mx-auto shadow-lg"
                      />
                    </div>
                  )}
                  {result.localization && (
  <div className="bg-black bg-opacity-30 p-4 rounded-lg">
    <h4 className="text-teal-300 font-semibold mb-4">🧩 Manipulation Localization</h4>
    <p className="text-gray-400 text-sm mb-4">
      Highlighted regions show manipulated or tampered areas.
    </p>
    <img
      src={`data:image/png;base64,${result.localization}`}
      alt="Localized Manipulation"
      className="rounded-lg border border-teal-500 border-opacity-30 max-w-full h-48 object-contain mx-auto shadow-lg"
    />
  </div>
)}

                </div>
              </div>
            )}

            {/* Video Detection Module */}
            {currentPage === "video" && (
                <>
                  <div className="mb-8 text-center">
                    <h3 className="text-3xl font-bold text-purple-400 mb-4">🎬 Video Analysis Module</h3>
                    <p className="text-gray-300">Upload your video for AI-powered deepfake detection</p>
                    <p className="text-purple-400 text-sm mt-2">✅ Connected to Firebase Database</p>
                  </div>

                  <div className="bg-gradient-to-br from-purple-900 via-indigo-900 to-violet-900 bg-opacity-40 backdrop-blur-sm border border-purple-500 border-opacity-30 p-12 rounded-xl shadow-2xl w-96 text-center">

                    {/* File Upload */}
                    <div className="border-2 border-dashed border-purple-400 border-opacity-50 rounded-lg p-8 mb-6 hover:border-opacity-100 transition-all duration-300">
                      <input
                        type="file"
                        accept="video/*"
                        onChange={handleFileChange}
                        className="hidden"
                        id="video-upload"
                      />
                      <label
                        htmlFor="video-upload"
                        className="cursor-pointer flex flex-col items-center justify-center"
                      >
                        <div className="w-16 h-16 mb-4 text-purple-400">
                          <svg fill="currentColor" viewBox="0 0 20 20">
                            <path d="M2 6a2 2 0 012-2h6l2 2h6a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/>
                            <path d="M8 7v6l5-3-5-3z"/>
                          </svg>
                        </div>
                        <span className="text-purple-400 font-semibold text-lg">
                          {file ? file.name : "🎥 Choose Video"}
                        </span>
                        <span className="text-gray-400 text-sm mt-2">
                          Click to upload a video for detection
                        </span>
                      </label>
                    </div>

                    {error && (
                      <div className="mb-4 p-3 bg-red-900 bg-opacity-50 border border-red-500 border-opacity-50 rounded-lg">
                        <p className="text-red-300 text-sm">{error}</p>
                      </div>
                    )}

                    {/* Analyze Button */}
                    <button
                      onClick={handleSubmit}
                      disabled={!file || loading}
                      className="w-full px-6 py-3 bg-purple-500 hover:bg-purple-600 rounded-lg font-semibold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {loading ? "🔄 ANALYZING VIDEO..." : "🚀 ANALYZE VIDEO"}
                    </button>

                    <p className="text-gray-400 text-sm mt-4">
                      📋 Supported: MP4, AVI, MOV, WEBM
                    </p>
                  </div>
                    {loading && currentPage === "video" && (
  <div className="mt-6 p-6 bg-purple-900 bg-opacity-30 border border-purple-500 rounded-xl max-w-3xl mx-auto">
    <h3 className="text-xl font-bold text-purple-300 mb-3">
      🎬 Video Analysis in Progress
    </h3>

    <p className="text-gray-300 mb-4">
      Video deepfake detection takes longer than image analysis because the system
      examines the video <strong>frame by frame</strong>.
    </p>

    <ul className="text-gray-300 text-sm space-y-2 list-disc list-inside">
      <li>Extracting key frames from the video</li>
      <li>Detecting and tracking faces across frames</li>
      <li>Analyzing motion and facial consistency</li>
      <li>Generating an annotated output video</li>
    </ul>

    {estimatedTime && (
  <p className="text-purple-300 mt-4 text-sm">
    ⏳ Estimated processing time: <strong>{estimatedTime}–{estimatedTime + 2} minutes</strong>
    <br />
    (Based on video length and system load)
  </p>
)}

    <div className="mt-4 flex items-center gap-3">
      <div className="w-4 h-4 rounded-full bg-purple-400 animate-pulse"></div>
      <span className="text-purple-200 text-sm">
        Please don’t refresh the page while processing
      </span>
    </div>
  </div>
)}

                  {/* Video Results */}
{videoResult && currentPage === "video" && (
  <div className="mt-10 p-6 bg-purple-900 bg-opacity-30 border border-purple-500 rounded-xl w-full max-w-4xl mx-auto">

    <h3 className="text-2xl font-bold text-purple-300 mb-4">
      🎬 Video Deepfake Analysis Results
    </h3>
    <button
  onClick={async () => {
    const res = await fetch("http://127.0.0.1:5000/download-video-report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
      filename: file.name,
      prediction: videoResult.prediction,
      confidence: videoResult.confidence,
      sessionId: videoResult.sessionId
    })
    });

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "video_deepfake_report.pdf";
    a.click();
  }}
  className="mt-4 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold"
>
  📄 Download Video Report
</button>


    <p className="text-gray-300 mb-6">
      The uploaded video was analyzed using advanced AI models that examine
      facial movements, lip-sync accuracy, and frame-to-frame consistency.
    </p>

    {/* Metrics */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div className="bg-black bg-opacity-30 p-4 rounded-lg text-center">
        <h4 className="text-purple-300 font-semibold mb-1">Prediction</h4>
        <p className={`text-2xl font-bold ${
          videoResult.prediction === "REAL" ? "text-green-400" : "text-red-400"
        }`}>
          {videoResult.prediction}
        </p>
      </div>

      <div className="bg-black bg-opacity-30 p-4 rounded-lg text-center">
        <h4 className="text-purple-300 font-semibold mb-1">Confidence</h4>
        <p className="text-2xl font-bold text-white">
          {videoResult.confidence}%
        </p>
      </div>

      <div className="bg-black bg-opacity-30 p-4 rounded-lg text-center">
        <h4 className="text-purple-300 font-semibold mb-1">Status</h4>
        <p className="text-green-400 font-bold">Complete</p>
      </div>
    </div>

    {/* Explanation */}
    <p className="text-gray-300 text-sm mb-4">
      The annotated video below highlights regions and frames where the AI
      detected potential manipulation patterns.
    </p>

    {/* Video */}
    <div className="flex justify-center mb-6">
      <div className="w-full max-w-2xl bg-black bg-opacity-40 border border-purple-500 rounded-xl p-4">
        <video
          controls
          playsInline
          className="w-full max-h-[360px] rounded-lg object-contain bg-black"
          src={videoResult.video_url}
        />
      </div>
    </div>

    {/* Download */}
    <div className="text-center">
      <button
  onClick={async () => {
    try {
      const response = await fetch(videoResult.video_url);
      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = "annotated_output.mp4";

      document.body.appendChild(link);
      link.click();

      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Failed to download video.");
    }
  }}
  className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold"
>
  ▶️ View / Download Annotated Video
      </button>


      <p className="text-gray-400 text-sm mt-2">
        Download the AI-annotated video for further review or reporting
      </p>
    </div>

  </div>
)}


                </>
            )}


            {/* Audio Detection Module */}
            {currentPage === "audio" && (
              <>
                <div className="mb-8 text-center">
                  <h3 className="text-3xl font-bold text-orange-400 mb-4">🎵 Audio Analysis Module</h3>
                  <p className="text-gray-300">Upload your audio for AI-generated speech detection</p>
                </div>
                
                <div className="bg-gradient-to-br from-orange-900 via-red-900 to-pink-900 bg-opacity-40 backdrop-blur-sm border border-orange-500 border-opacity-30 p-12 rounded-xl shadow-2xl w-96 text-center">
                  <div className="border-2 border-dashed border-orange-400 border-opacity-50 rounded-lg p-8 mb-6 hover:border-opacity-100 transition-all duration-300 hover:shadow-orange-400/20">
                    <input
                      type="file"
                      accept="audio/*"
                      onChange={handleFileChange}
                      className="hidden"
                      id="audio-upload"
                    />

                    <label
                      htmlFor="audio-upload"
                      className="cursor-pointer flex flex-col items-center justify-center"
                    >
                      <Mic className="text-orange-400 mb-4" size={64} />
                      <span className="text-orange-400 font-semibold text-lg">
                        {file ? file.name : "🎧 Choose Audio File"}
                      </span>
                      <span className="text-gray-400 text-sm mt-2">
                        Click to upload audio for detection
                      </span>
                    </label>
                  </div>
                  {error && (
                    <div className="mb-4 p-3 bg-red-900 bg-opacity-50 border border-red-500 border-opacity-50 rounded-lg">
                      <p className="text-red-300 text-sm">{error}</p>
                    </div>
                  )}

                  <button
                    onClick={handleSubmit}
                    disabled={!file || loading}
                    className="w-full px-6 py-3 bg-orange-500 hover:bg-orange-600 rounded-lg font-semibold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? "🔄 ANALYZING AUDIO..." : "🎧 ANALYZE AUDIO"}
                  </button>

                  <p className="text-gray-400 text-sm mt-4">
                    📋 Supported: MP3, WAV, FLAC, M4A
                  </p>

                </div>
              </>
              
            )}
            {/* Audio Results Display */}
              {audioResult && currentPage === "audio" && (
                <div className="mt-8 p-6 bg-orange-900 bg-opacity-30 border border-orange-500 rounded-lg max-w-3xl mx-auto text-center shadow-xl">
                  
                  <h3 className="text-2xl font-bold text-orange-400 mb-4">
                    🎧 Audio Deepfake Analysis Results
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                      <h4 className="text-orange-300 font-semibold mb-2">Prediction</h4>
                      <p className={`text-2xl font-bold ${
                        audioResult.prediction === "REAL" ? "text-green-400" : "text-red-400"
                      }`}>
                        {audioResult.prediction}
                      </p>
                    </div>

                    <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                      <h4 className="text-orange-300 font-semibold mb-2">Confidence</h4>
                      <p className="text-2xl font-bold text-white">
                        {audioResult.confidence}%
                      </p>
                    </div>

                    <div className="bg-black bg-opacity-30 p-4 rounded-lg">
                      <h4 className="text-orange-300 font-semibold mb-2">Risk Level</h4>
                      <p className={`text-lg font-bold ${
                        audioResult.risk === "HIGH" ? "text-red-400" : "text-green-400"
                      }`}>
                        {audioResult.risk}
                      </p>
                    </div>
                  </div>

                  
                  <div className="mt-6 bg-black bg-opacity-30 p-4 rounded-lg">
                      <h4 className="text-orange-300 font-semibold mb-3">
                        🎵 Audio Timeline - Listen to the Analyzed Audio
                      </h4>

                      <div ref={waveformRef} />

                      <div className="flex justify-center mt-3 gap-4">
                        <button
                          onClick={() => waveSurferRef.current?.playPause()}
                          className="bg-orange-600 px-4 py-2 rounded text-white"
                        >
                          ▶️ Play / Pause
                        </button>
                      </div>
                    </div>

                  {/* Waveform Visualization */}
                  <div ref={waveformRef} className="w-full mt-4"></div>
                  {/* Spectrogram Visualization */}
              {audioResult.spectrogram && (
                <div className="mt-6 bg-black bg-opacity-30 p-4 rounded-lg">
                  <h4 className="text-orange-300 font-semibold mb-3">
                    🔥 AI Attention Map (Spectrogram)
                  </h4>
                  <p className="text-gray-400 text-sm mb-3">
                    Highlighted regions indicate time–frequency patterns that influenced the model decision.
                  </p>
                  <img
                    src={`data:image/png;base64,${audioResult.spectrogram}`}
                    alt="Audio Spectrogram"
                    className="rounded-lg border border-orange-500 max-w-full mx-auto"
                  />
                </div>
              )}
              {/* Download Audio Report */}
              <div className="mt-6 text-center">
                <button
                  onClick={async () => {
                    try {
                      const res = await fetch("http://127.0.0.1:5000/download-audio-report", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                        fileName: file?.name,
                        prediction: audioResult.prediction,
                        confidence: audioResult.confidence,
                        spectrogram: audioResult.spectrogram,
                        segments: audioResult.segments,
                        sessionId: audioResult.sessionId
                      })
                      });

                      const blob = await res.blob();
                      const url = window.URL.createObjectURL(blob);
                      const a = document.createElement("a");

                      a.href = url;
                      a.download = "forge_detect_audio_report.pdf";
                      a.click();

                      window.URL.revokeObjectURL(url);
                    } catch (err) {
                      alert("Failed to download audio report");
                    }
                  }}
                  className="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700
                            text-white font-bold py-3 px-8 rounded-lg shadow-lg transition-all duration-300"
                >
                  📄 Download Audio Analysis Report
                </button>

                <p className="text-gray-400 text-sm mt-2">
                  Includes prediction summary and AI spectrogram analysis
                </p>
              </div>

            {/* Segment-wise Analysis */}
              {audioResult.segments && (
                <div className="mt-6 bg-black bg-opacity-30 p-4 rounded-lg">
                  <h4 className="text-orange-300 font-semibold mb-3">
                    ⏱️ Temporal Segment Analysis
                  </h4>

                  <ul className="text-sm text-gray-300 space-y-2">
                    {audioResult.segments.map((seg, idx) => (
                      <li key={idx}>
                        {seg.start}s – {seg.end}s :
                        <span className={
                          seg.fake_score > 0.7 ? "text-red-400 ml-2" :
                          seg.fake_score > 0.4 ? "text-yellow-400 ml-2" :
                          "text-green-400 ml-2"
                        }>
                          Fake likelihood: {(seg.fake_score * 100).toFixed(1)}%
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
                </div>
              )}
            

          </section>
        </>
      )}

      {/* Footer */}
      <footer className="py-12 bg-black bg-opacity-50">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 px-10 max-w-4xl mx-auto">
          <div>
            <h4 className="text-xl font-semibold text-teal-400 mb-4">About Us</h4>
            <p className="text-gray-300 leading-relaxed">
              We are building a comprehensive deepfake detection platform using cutting-edge AI to combat digital deception across images, videos, and audio content.
            </p>
          </div>
          <div>
            <h4 className="text-xl font-semibold text-teal-400 mb-4">Legal</h4>
            <p className="text-gray-300 hover:text-teal-400 cursor-pointer">Privacy Policy</p>
            <p className="text-gray-300 hover:text-teal-400 cursor-pointer">Terms of Service</p>
          </div>
        </div>
        <div className="text-center text-gray-400 mt-8">
          <p>© 2025 Forge Detect. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );

}

export default App;