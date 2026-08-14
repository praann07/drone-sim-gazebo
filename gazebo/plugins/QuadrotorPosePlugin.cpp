#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <ignition/math/Pose3.hh>

#include <iostream>
#include <sstream>
#include <thread>
#include <atomic>
#include <mutex>
#include <string>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

namespace gazebo
{
  class QuadrotorPosePlugin : public ModelPlugin
  {
    private: physics::ModelPtr model;
    private: event::ConnectionPtr updateConnection;
    private: std::thread receiverThread;
    private: std::atomic<bool> running{true};
    private: std::mutex poseMutex;
    private: ignition::math::Pose3d targetPose;
    private: bool hasNewPose = false;

    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/) override
    {
      this->model = _parent;
      this->targetPose = this->model->WorldPose();
      this->model->SetGravityMode(false);

      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&QuadrotorPosePlugin::OnUpdate, this));

      this->receiverThread = std::thread(&QuadrotorPosePlugin::TcpReceiver, this);
      gzmsg << "[QuadrotorPosePlugin] Live Telemetry Plugin active on TCP port 9099!\n";
    }

    public: ~QuadrotorPosePlugin()
    {
      this->running = false;
      if (this->receiverThread.joinable())
      {
        this->receiverThread.detach();
      }
    }

    private: void TcpReceiver()
    {
      int server_fd = socket(AF_INET, SOCK_STREAM, 0);
      if (server_fd < 0) return;

      int opt = 1;
      setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

      sockaddr_in address{};
      address.sin_family = AF_INET;
      address.sin_addr.s_addr = INADDR_ANY;
      address.sin_port = htons(9099);

      if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
      {
        close(server_fd);
        return;
      }

      if (listen(server_fd, 3) < 0)
      {
        close(server_fd);
        return;
      }

      gzmsg << "[QuadrotorPosePlugin] Listening for telemetry on TCP port 9099...\n";

      while (this->running)
      {
        sockaddr_in client_addr{};
        socklen_t addrlen = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &addrlen);
        if (client_fd < 0)
        {
          usleep(50000);
          continue;
        }

        gzmsg << "[QuadrotorPosePlugin] Connected to Windows Python GCS!\n";

        std::string buffer = "";
        char temp[2048];

        while (this->running)
        {
          ssize_t bytes = recv(client_fd, temp, sizeof(temp) - 1, 0);
          if (bytes <= 0) break;

          temp[bytes] = '\0';
          buffer += temp;

          size_t newline_pos;
          while ((newline_pos = buffer.find('\n')) != std::string::npos)
          {
            std::string line = buffer.substr(0, newline_pos);
            buffer.erase(0, newline_pos + 1);

            while (!line.empty() && (line.back() == '\r' || line.back() == ' '))
            {
              line.pop_back();
            }

            if (line.empty()) continue;

            double x = 0.0, y = 0.0, z = 0.05, roll = 0.0, pitch = 0.0, yaw = 0.0;
            bool valid = false;

            if (line[0] == '{')
            {
              // Parse JSON: {"x": ..., "y": ..., "z": ..., "roll": ..., "pitch": ..., "yaw": ...}
              auto parseVal = [&](const std::string &key, double &val) {
                size_t pos = line.find("\"" + key + "\"");
                if (pos != std::string::npos) {
                  size_t colon = line.find(":", pos);
                  if (colon != std::string::npos) {
                    val = std::stod(line.substr(colon + 1));
                  }
                }
              };

              try {
                parseVal("x", x);
                parseVal("y", y);
                parseVal("z", z);
                parseVal("roll", roll);
                parseVal("pitch", pitch);
                parseVal("yaw", yaw);
                valid = true;
              } catch (...) {}
            }
            else
            {
              // Parse CSV: POSE,x,y,z,roll,pitch,yaw
              try {
                std::stringstream ss(line);
                std::string tag, sx, sy, sz, sroll, spitch, syaw;
                if (std::getline(ss, tag, ',') && tag == "POSE" &&
                    std::getline(ss, sx, ',') &&
                    std::getline(ss, sy, ',') &&
                    std::getline(ss, sz, ','))
                {
                  x = std::stod(sx);
                  y = std::stod(sy);
                  z = std::stod(sz);
                  if (std::getline(ss, sroll, ',')) roll = std::stod(sroll);
                  if (std::getline(ss, spitch, ',')) pitch = std::stod(spitch);
                  if (std::getline(ss, syaw, ',')) yaw = std::stod(syaw);
                  valid = true;
                }
              } catch (...) {}
            }

            if (valid)
            {
              ignition::math::Vector3d pos(x, y, z);
              ignition::math::Quaterniond rot(roll, pitch, yaw);
              ignition::math::Pose3d pose(pos, rot);

              {
                std::lock_guard<std::mutex> lock(this->poseMutex);
                this->targetPose = pose;
                this->hasNewPose = true;
              }

              this->model->SetWorldPose(pose);
              this->model->ResetPhysicsStates();
            }
          }
        }
        close(client_fd);
      }
      close(server_fd);
    }

    public: void OnUpdate()
    {
      ignition::math::Pose3d p;
      bool updateNeeded = false;
      {
        std::lock_guard<std::mutex> lock(this->poseMutex);
        if (this->hasNewPose)
        {
          p = this->targetPose;
          this->hasNewPose = false;
          updateNeeded = true;
        }
      }
      if (updateNeeded)
      {
        this->model->SetWorldPose(p);
        this->model->ResetPhysicsStates();
      }
    }
  };

  GZ_REGISTER_MODEL_PLUGIN(QuadrotorPosePlugin)
}
