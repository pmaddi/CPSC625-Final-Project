#include <iostream>
#include <string>
#include <type_traits>
#include <vector>
#include <map>
#include <string>

using Dependency = std::pair<int, int>;
using DependencyList = std::vector<Dependency>;
using Data = int;
using Id = int;
using Index = int;
using NodeValue = std::pair<DependencyList, Data>;
using NodeValuePtr = std::shared_ptr<NodeValue>;
class Database {
    public :
        Database();
        NodeValuePtr get(Id id, Index index);
        int set(Id id, Index index, const NodeValue& node_value);
        Index get_global_horizon(Id id);
        Index set_global_horizon(Id id, Index new_horizon);
    private :
        std::map<std::string, NodeValue> _map;
        std::map<std::string, Index> _g_horizon;
};

class BaseLocalView {
    public :
        BaseLocalView();
        virtual int upcall(Id id, Data data);
};

class Runtime {
    public :
        Runtime(Database& db, BaseLocalView& local_view);
        int append(Id id, DependencyList dependencies, Data data);
        int read_next(Id id);
        int play_forward(Id id);
    private :
        Index get_local_horizon(Id id);
        Index set_local_horizon(Id id, Index new_horizon);
        int read(Id id, int index);
        Database& _db;
        BaseLocalView& _local_view;
        std::map<std::string, Index> _local_horizon;
};

Database::Database() {
}
NodeValuePtr Database::get(Id id, Index index) {
    auto id_str = std::to_string(id);
    auto index_str  = std::to_string(index);
    auto key = id_str + ":" + index_str;
    auto it = _map.find(key);
    if (it == _map.end()) {
        return std::shared_ptr<NodeValue>(0);
    } else {
        return std::shared_ptr<NodeValue>(&(it->second));
    }
}
int Database::set(Id id, Index index, const NodeValue& node_value) {
    auto id_str = std::to_string(id);
    auto index_str  = std::to_string(index);
    auto key = id_str + ":" + index_str;
    _map.insert(std::pair<std::string, NodeValue>(key, node_value));
    return 0;
}
Index Database::get_global_horizon(Id id) {
    auto it  = _g_horizon.find(std::to_string(id) + ":count");
    if (it == _g_horizon.end()) {
        return 0;
    } else {
        return it->second;
    }
}
Index Database::set_global_horizon(Id id, Index new_horizon) {
    _g_horizon.insert(std::pair<std::string, Index>(
                std::to_string(id) + ":count",
                new_horizon));
    return new_horizon;
}

Runtime::Runtime(Database& db, BaseLocalView& local_view) 
    : _db(db), _local_view(local_view) {
}
Index Runtime::get_local_horizon(Id id) {
    auto it  = _local_horizon.find(std::to_string(id) + ":count");
    if (it == _local_horizon.end()) {
        return 0;
    } else {
        return it->second;
    }
}
Index Runtime::set_local_horizon(Id id, Index new_horizon) {
    _local_horizon.insert(std::pair<std::string, Index>(
                std::to_string(id) + ":count",
                new_horizon));
    return new_horizon;
}
int Runtime::append(Id id, DependencyList dependencies, Data data) {
    auto horizion = _db.get_global_horizon(id);
    _db.set(id, horizion + 1, NodeValue(dependencies, data));
    _db.set_global_horizon(id, horizion + 1);
    return 0;
}
int Runtime::read_next(Id id) {
    auto seen = get_local_horizon(id);
    return read(id, seen + 1);
}
int Runtime::read(Id id, Index index) {
    if (get_local_horizon(id) >= index) {
        return -1;
    }
    auto val = _db.get(id, index);
    if (val) {
        
    } else {
        return -1;
    }

    return 0;

}








    
    



int main() {
    std::cout << "hi";
}
