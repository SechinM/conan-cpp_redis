#include <cpp_redis/cpp_redis>

int main(int argc, char *argv[])
{
	std::shared_ptr<cpp_redis::redis_client> client_;
	client_.reset(new cpp_redis::redis_client());
	try {
		std::cout << "In Connect" << std::endl;
		client_->connect("127.0.0.1", 6379, [](cpp_redis::redis_client &) {
			std::cout << "client disconnected (disconnection handler)" << std::endl;
			should_exit = true;
		});
	}
	catch (std::exception const& e) {
		std::cerr << e.what() << std::endl;
	}

	return 0;
}
