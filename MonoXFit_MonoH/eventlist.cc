#include <map>
#include <set>
#include <fstream>
#include <stdexcept>
#include <string>
#include <cstdlib>
#include <iostream>

typedef std::map<unsigned, std::set<unsigned> > EventList;

EventList
readEventList(char const* _fileName)
{
  EventList list;
  ifstream listFile(_fileName);
  if (!listFile.is_open())
    throw std::runtime_error(_fileName);

  unsigned iL(0);
  std::string line;
  while (true) {
    std::getline(listFile, line);
    if (!listFile.good())
      break;
    
    if (line.find(":") == std::string::npos || line.find(":") == line.rfind(":"))
      continue;

    unsigned run(std::atoi(line.substr(0, line.find(":")).c_str()));
    unsigned event(std::atoi(line.substr(line.rfind(":") + 1).c_str()));

    list[run].insert(event);

    ++iL;
  }

  std::cout << "Loaded " << iL << " events" << std::endl;

  return list;
}

// Usage:
// auto rItr(list.find(run));
// if (rItr != list.end()) {
//   auto eItr(rItr->second.find(event));
//   if (eItr != list.end())
//     /* SKIP EVENT */
// }
